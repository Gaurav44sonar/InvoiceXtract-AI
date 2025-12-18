import { Download, Save, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ExtractedInvoiceData } from "@/services/api";
import { toast } from "@/hooks/use-toast";
import { useInvoiceHistory } from "@/hooks/useInvoiceHistory";

interface InvoiceResultsProps {
  data: ExtractedInvoiceData;
  fileName: string;
  onBack: () => void;
}

const InvoiceResults = ({ data, fileName, onBack }: InvoiceResultsProps) => {
  const { saveToHistory } = useInvoiceHistory();

  /* ---------------------------
     Download JSON
  --------------------------- */
  const handleDownloadJSON = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `invoice_${data.invoice_number || "extracted"}.json`;
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast({
      title: "Downloaded",
      description: "Invoice JSON downloaded successfully",
    });
  };

  /* ---------------------------
     Save to MongoDB
  --------------------------- */
  const handleSave = async () => {
    try {
      await saveToHistory(fileName, data);
      toast({
        title: "Saved",
        description: "Invoice saved to database",
      });
    } catch (err: any) {
      toast({
        title: "Save failed",
        description: err?.message || "Unable to save invoice",
        variant: "destructive",
      });
    }
  };

  /* ---------------------------
     Helpers
  --------------------------- */
  const formatCurrency = (value?: number) =>
    value === undefined
      ? "—"
      : new Intl.NumberFormat("en-IN", {
          style: "currency",
          currency: data.currency || "INR",
        }).format(value);

  const formatDate = (date: string) => {
    try {
      return new Date(date).toLocaleDateString("en-IN", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    } catch {
      return date;
    }
  };

  return (
    <div className="space-y-6 animate-slide-up">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back
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

      {/* Invoice Summary */}
      <div className="bg-card rounded-2xl shadow-card p-6 md:p-8">
        <h2 className="text-2xl font-bold text-foreground mb-6">
          Extracted Invoice Data
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <Detail label="Invoice Number" value={data.invoice_number || "—"} />
          <Detail label="Invoice Date" value={formatDate(data.invoice_date)} />
          <Detail label="Vendor" value={data.vendor?.name || "—"} />
          <Detail label="Subtotal" value={formatCurrency(data.subtotal)} />
          <Detail label="Tax" value={formatCurrency(data.tax_amount)} />
          <Detail label="Total" value={formatCurrency(data.total)} accent />
        </div>

        {/* Line Items */}
        {data.items?.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Line Items</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-2">Description</th>
                    <th className="text-right py-2">Qty</th>
                    <th className="text-right py-2">Total</th>
                  </tr>
                </thead>
                <tbody>
                  {data.items.map((item, i) => (
                    <tr key={i} className="border-b border-border/50">
                      <td className="py-2">{item.description}</td>
                      <td className="py-2 text-right">{item.quantity}</td>
                      <td className="py-2 text-right">
                        {formatCurrency(item.total)}
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

/* ---------------------------
   Detail Card
--------------------------- */
const Detail = ({
  label,
  value,
  accent,
}: {
  label: string;
  value: string;
  accent?: boolean;
}) => (
  <div className={`p-4 rounded-xl ${accent ? "bg-accent/10" : "bg-secondary/50"}`}>
    <p className="text-sm text-muted-foreground mb-1">{label}</p>
    <p className={`text-lg font-semibold ${accent ? "text-accent" : ""}`}>
      {value}
    </p>
  </div>
);

export default InvoiceResults;
