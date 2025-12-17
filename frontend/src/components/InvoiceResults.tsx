import { Download, Save, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ExtractedInvoiceData } from '@/services/api';
import { toast } from '@/hooks/use-toast';

interface InvoiceResultsProps {
  data: ExtractedInvoiceData;
  onBack: () => void;
  onSave: () => void;
}

const InvoiceResults = ({ data, onBack, onSave }: InvoiceResultsProps) => {
  const handleDownloadJSON = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `invoice_${data.invoice_number || 'extracted'}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast({
      title: "Downloaded!",
      description: "Invoice data saved as JSON file.",
    });
  };

  const handleSave = () => {
    onSave();
    toast({
      title: "Saved!",
      description: "Invoice has been saved to history.",
    });
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch {
      return dateString;
    }
  };

  return (
    <div className="space-y-6 animate-slide-up">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <Button variant="ghost" onClick={onBack} className="self-start">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Upload
        </Button>
        <div className="flex gap-3">
          <Button variant="outline" onClick={handleDownloadJSON}>
            <Download className="mr-2 h-4 w-4" />
            Download JSON
          </Button>
          <Button variant="success" onClick={handleSave}>
            <Save className="mr-2 h-4 w-4" />
            Save Result
          </Button>
        </div>
      </div>

      {/* Invoice Details Card */}
      <div className="bg-card rounded-2xl shadow-card p-6 md:p-8">
        <h2 className="text-2xl font-bold text-foreground mb-6">Extracted Invoice Data</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <DetailCard label="Invoice Number" value={data.invoice_number || 'N/A'} />
          <DetailCard label="Invoice Date" value={formatDate(data.invoice_date)} />
          <DetailCard label="Vendor Name" value={data.vendor_name || 'N/A'} />
          <DetailCard 
            label="GST Amount" 
            value={formatCurrency(data.gst_amount || 0)} 
            highlight 
          />
          <DetailCard 
            label="Total Amount" 
            value={formatCurrency(data.total_amount || 0)} 
            highlight
            accent
          />
        </div>

        {/* Line Items Table */}
        {data.line_items && data.line_items.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-4">Line Items</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Description</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Qty</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Unit Price</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {data.line_items.map((item, index) => (
                    <tr 
                      key={index} 
                      className="border-b border-border/50 hover:bg-secondary/50 transition-colors"
                    >
                      <td className="py-4 px-4 text-sm text-foreground">{item.description}</td>
                      <td className="py-4 px-4 text-sm text-foreground text-right">{item.quantity}</td>
                      <td className="py-4 px-4 text-sm text-foreground text-right">
                        {formatCurrency(item.unit_price)}
                      </td>
                      <td className="py-4 px-4 text-sm font-medium text-foreground text-right">
                        {formatCurrency(item.amount)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

interface DetailCardProps {
  label: string;
  value: string;
  highlight?: boolean;
  accent?: boolean;
}

const DetailCard = ({ label, value, highlight, accent }: DetailCardProps) => (
  <div className={`p-4 rounded-xl ${highlight ? (accent ? 'bg-accent/10' : 'bg-primary/5') : 'bg-secondary/50'}`}>
    <p className="text-sm text-muted-foreground mb-1">{label}</p>
    <p className={`text-lg font-semibold ${accent ? 'text-accent' : highlight ? 'text-primary' : 'text-foreground'}`}>
      {value}
    </p>
  </div>
);

export default InvoiceResults;
