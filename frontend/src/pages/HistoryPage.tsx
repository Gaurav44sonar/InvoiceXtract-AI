import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import { Button } from "@/components/ui/button";
import { InvoiceHistoryItem, ExtractedInvoiceData } from "@/services/api";
import api from "@/services/api";
import {
  FileText,
  CheckCircle,
  XCircle,
  Clock,
  Upload,
  Calendar,
  Download,
  Eye,
  X,
} from "lucide-react";
import { Link } from "react-router-dom";
import { toast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";

const HistoryPage = () => {
  const [history, setHistory] = useState<InvoiceHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedInvoice, setSelectedInvoice] =
    useState<InvoiceHistoryItem | null>(null);

  /* ---------------------------
     Fetch invoices
  --------------------------- */
  const fetchHistory = async () => {
    try {
      setIsLoading(true);
      const res = await api.get("/invoices");
      setHistory(res.data);
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to load invoice history",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  /* ---------------------------
     Helpers
  --------------------------- */
  const getStatusIcon = (status: string) => {
    if (status === "processed")
      return <CheckCircle className="h-4 w-4 text-success" />;
    if (status === "failed")
      return <XCircle className="h-4 w-4 text-destructive" />;
    return <Clock className="h-4 w-4 text-warning animate-pulse" />;
  };

 const formatDate = (dateString?: string) => {
  if (!dateString) return "—";
  const d = new Date(dateString);
  return isNaN(d.getTime())
    ? "—"
    : d.toLocaleDateString("en-IN", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
};


const parseNumber = (v: any): number | null => {
  if (v === null || v === undefined || v === "") return null;
  const cleaned = String(v).replace(/[^0-9.-]+/g, "");
  const n = Number(cleaned);
  return Number.isFinite(n) ? n : null;
};

const formatCurrency = (value: any) => {
  const n = parseNumber(value);
  if (n === null) return "—";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
  }).format(n);
};


  const downloadJSON = (data: ExtractedInvoiceData, fileName: string) => {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${fileName.replace(".pdf", "")}_data.json`;
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
     UI
  --------------------------- */
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="container py-8 md:py-12">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold">
              Invoice History
            </h1>
            <p className="text-muted-foreground">
              Previously processed invoices
            </p>
          </div>
          <Button variant="hero" asChild>
            <Link to="/upload">
              <Upload className="mr-2 h-4 w-4" />
              Upload New
            </Link>
          </Button>
        </div>

        {/* Loading */}
        {isLoading ? (
          <p className="text-muted-foreground text-center">
            Loading invoices...
          </p>
        ) : history.length === 0 ? (
          <div className="bg-card p-10 rounded-xl text-center">
            <FileText className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">
              No invoices found
            </p>
          </div>
        ) : (
          <div className="grid gap-4">
            {history.map((inv) => (
              <div
                key={inv.id}
                className="bg-card rounded-xl p-6 shadow-card flex items-center gap-4"
              >
                <div className="h-12 w-12 bg-secondary rounded-lg flex items-center justify-center">
                  <FileText className="h-6 w-6 text-destructive" />
                </div>

                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h3 className="font-medium truncate">
                      {inv.file_name}
                    </h3>
                    <span
                      className={cn(
                        "text-xs px-2 py-1 rounded-full capitalize flex items-center gap-1",
                        inv.status === "processed"
                          ? "bg-success/10 text-success"
                          : "bg-warning/10 text-warning"
                      )}
                    >
                      {getStatusIcon(inv.status)}
                      {inv.status}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                    <Calendar className="h-4 w-4" />
                    {formatDate(inv.upload_date)}
                  </p>
                </div>

                {/* {inv.data && (
                  <span className="font-semibold text-accent">
                    {formatCurrency(inv.data.total)}
                  </span>
                )} */}
                {inv.data && (
  <span className="font-semibold text-accent">
    {formatCurrency(inv.data?.total_amount)}
  </span>
)}


                <div className="flex gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setSelectedInvoice(inv)}
                  >
                    <Eye className="h-4 w-4" />
                  </Button>
                  {inv.data && (
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() =>
                        downloadJSON(inv.data!, inv.file_name)
                      }
                    >
                      <Download className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Modal */}
      {selectedInvoice && selectedInvoice.data && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-xl max-w-xl w-full p-6 relative">
            <Button
              variant="ghost"
              size="icon"
              className="absolute top-3 right-3"
              onClick={() => setSelectedInvoice(null)}
            >
              <X className="h-5 w-5" />
            </Button>

            <h2 className="text-xl font-bold mb-4">
              Invoice Details
            </h2>

            <pre className="text-sm bg-secondary/50 p-4 rounded-lg overflow-auto max-h-[60vh]">
              {JSON.stringify(selectedInvoice.data, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default HistoryPage;
