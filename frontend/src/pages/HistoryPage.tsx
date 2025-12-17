import { useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { useInvoiceHistory } from '@/hooks/useInvoiceHistory';
import { InvoiceHistoryItem, ExtractedInvoiceData } from '@/services/api';
import { 
  FileText, 
  Image, 
  CheckCircle, 
  XCircle, 
  Clock, 
  Upload,
  ChevronRight,
  Calendar,
  Download,
  Eye,
  X
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from '@/hooks/use-toast';

const HistoryPage = () => {
  const { history, isLoading } = useInvoiceHistory();
  const [selectedInvoice, setSelectedInvoice] = useState<InvoiceHistoryItem | null>(null);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'processed':
        return <CheckCircle className="h-4 w-4 text-success" />;
      case 'failed':
        return <XCircle className="h-4 w-4 text-destructive" />;
      default:
        return <Clock className="h-4 w-4 text-warning animate-pulse" />;
    }
  };

  const getStatusBadge = (status: string) => {
    const styles = {
      processed: 'bg-success/10 text-success',
      failed: 'bg-destructive/10 text-destructive',
      processing: 'bg-warning/10 text-warning',
    };

    return (
      <span className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium capitalize",
        styles[status as keyof typeof styles] || styles.processing
      )}>
        {getStatusIcon(status)}
        {status}
      </span>
    );
  };

  const getFileIcon = (fileName: string) => {
    if (fileName.toLowerCase().endsWith('.pdf')) {
      return <FileText className="h-5 w-5 text-destructive" />;
    }
    return <Image className="h-5 w-5 text-accent" />;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  };

  const handleDownloadJSON = (data: ExtractedInvoiceData, fileName: string) => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${fileName.split('.')[0]}_data.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast({
      title: "Downloaded!",
      description: "Invoice data saved as JSON file.",
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container py-8 md:py-12">
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
              Invoice History
            </h1>
            <p className="text-muted-foreground">
              View and manage your previously processed invoices
            </p>
          </div>
          <Button variant="hero" asChild>
            <Link to="/upload">
              <Upload className="mr-2 h-4 w-4" />
              Upload New
            </Link>
          </Button>
        </div>

        {/* Content */}
        {isLoading ? (
          <div className="grid gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-card rounded-xl p-6 animate-pulse">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-secondary rounded-lg" />
                  <div className="flex-1">
                    <div className="h-4 bg-secondary rounded w-1/3 mb-2" />
                    <div className="h-3 bg-secondary rounded w-1/4" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : history.length === 0 ? (
          <div className="bg-card rounded-2xl shadow-card p-12 text-center">
            <div className="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mx-auto mb-4">
              <FileText className="h-8 w-8 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-2">
              No invoices yet
            </h3>
            <p className="text-muted-foreground mb-6 max-w-md mx-auto">
              Upload your first invoice to get started with AI-powered data extraction.
            </p>
            <Button variant="hero" asChild>
              <Link to="/upload">
                <Upload className="mr-2 h-4 w-4" />
                Upload Invoice
              </Link>
            </Button>
          </div>
        ) : (
          <div className="grid gap-4">
            {history.map((invoice) => (
              <div
                key={invoice.id}
                className="bg-card rounded-xl shadow-card hover:shadow-card-hover transition-all duration-300 overflow-hidden group"
              >
                <div className="p-6">
                  <div className="flex items-center gap-4">
                    {/* File Icon */}
                    <div className="w-12 h-12 bg-secondary rounded-lg flex items-center justify-center flex-shrink-0">
                      {getFileIcon(invoice.file_name)}
                    </div>

                    {/* File Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-1">
                        <h3 className="font-medium text-foreground truncate">
                          {invoice.file_name}
                        </h3>
                        {getStatusBadge(invoice.status)}
                      </div>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Calendar className="h-3.5 w-3.5" />
                          {formatDate(invoice.upload_date)}
                        </span>
                        {invoice.data && (
                          <span className="font-medium text-accent">
                            {formatCurrency(invoice.data.total_amount)}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center gap-2">
                      {invoice.status === 'processed' && invoice.data && (
                        <>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => setSelectedInvoice(invoice)}
                            title="View Details"
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleDownloadJSON(invoice.data!, invoice.file_name)}
                            title="Download JSON"
                          >
                            <Download className="h-4 w-4" />
                          </Button>
                        </>
                      )}
                      <ChevronRight className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Detail Modal */}
      {selectedInvoice && selectedInvoice.data && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div 
            className="absolute inset-0 bg-foreground/20 backdrop-blur-sm"
            onClick={() => setSelectedInvoice(null)}
          />
          <div className="relative bg-card rounded-2xl shadow-xl max-w-2xl w-full max-h-[80vh] overflow-auto animate-scale-in">
            <div className="sticky top-0 bg-card border-b border-border p-4 flex items-center justify-between">
              <h2 className="text-xl font-bold text-foreground">Invoice Details</h2>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setSelectedInvoice(null)}
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
            
            <div className="p-6 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-secondary/50 rounded-xl">
                  <p className="text-sm text-muted-foreground mb-1">Invoice Number</p>
                  <p className="font-semibold text-foreground">{selectedInvoice.data.invoice_number}</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-xl">
                  <p className="text-sm text-muted-foreground mb-1">Date</p>
                  <p className="font-semibold text-foreground">{selectedInvoice.data.invoice_date}</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-xl col-span-2">
                  <p className="text-sm text-muted-foreground mb-1">Vendor</p>
                  <p className="font-semibold text-foreground">{selectedInvoice.data.vendor_name}</p>
                </div>
                <div className="p-4 bg-primary/5 rounded-xl">
                  <p className="text-sm text-muted-foreground mb-1">GST Amount</p>
                  <p className="font-semibold text-primary">{formatCurrency(selectedInvoice.data.gst_amount)}</p>
                </div>
                <div className="p-4 bg-accent/10 rounded-xl">
                  <p className="text-sm text-muted-foreground mb-1">Total Amount</p>
                  <p className="font-semibold text-accent">{formatCurrency(selectedInvoice.data.total_amount)}</p>
                </div>
              </div>

              {selectedInvoice.data.line_items.length > 0 && (
                <div>
                  <h3 className="font-semibold text-foreground mb-3">Line Items</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-border">
                          <th className="text-left py-2 font-medium text-muted-foreground">Description</th>
                          <th className="text-right py-2 font-medium text-muted-foreground">Qty</th>
                          <th className="text-right py-2 font-medium text-muted-foreground">Price</th>
                          <th className="text-right py-2 font-medium text-muted-foreground">Amount</th>
                        </tr>
                      </thead>
                      <tbody>
                        {selectedInvoice.data.line_items.map((item, idx) => (
                          <tr key={idx} className="border-b border-border/50">
                            <td className="py-3 text-foreground">{item.description}</td>
                            <td className="py-3 text-right text-foreground">{item.quantity}</td>
                            <td className="py-3 text-right text-foreground">{formatCurrency(item.unit_price)}</td>
                            <td className="py-3 text-right font-medium text-foreground">{formatCurrency(item.amount)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              <Button 
                variant="hero" 
                className="w-full"
                onClick={() => handleDownloadJSON(selectedInvoice.data!, selectedInvoice.file_name)}
              >
                <Download className="mr-2 h-4 w-4" />
                Download as JSON
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HistoryPage;
