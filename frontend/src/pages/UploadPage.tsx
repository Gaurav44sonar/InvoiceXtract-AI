import { useState, useCallback } from "react";
import Navbar from "@/components/Navbar";
import { Button } from "@/components/ui/button";
import FileUploadZone from "@/components/FileUploadZone";
import UploadProgress from "@/components/UploadProgress";
import InvoiceResults from "@/components/InvoiceResults";
import { useInvoiceUpload } from "@/hooks/useInvoiceUpload";
import { Upload, AlertCircle } from "lucide-react";

const UploadPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const {
    isUploading,
    uploadProgress,
    error,
    data,
    upload,
    reset,
  } = useInvoiceUpload();

  /* ---------------------------
     File select
  --------------------------- */
  const handleFileSelect = useCallback(
    (file: File) => {
      setSelectedFile(file);
      reset();
    },
    [reset]
  );

  /* ---------------------------
     Clear file
  --------------------------- */
  const handleClear = useCallback(() => {
    setSelectedFile(null);
    reset();
  }, [reset]);

  /* ---------------------------
     Upload
  --------------------------- */
  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      await upload(selectedFile);
    } catch {
      // error already handled by hook
    }
  };

  /* ---------------------------
     Back from result
  --------------------------- */
  const handleBack = () => {
    setSelectedFile(null);
    reset();
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="container py-8 md:py-12">
        {/* Page Header */}
        {!data && (
          <div className="text-center mb-10">
            <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-3">
              Upload Invoice
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto">
              Upload a PDF invoice and let AI extract the data automatically.
            </p>
          </div>
        )}

        <div className="max-w-3xl mx-auto">
          {/* Result */}
          {data && selectedFile ? (
            <InvoiceResults
              data={data}
              fileName={selectedFile.name}
              onBack={handleBack}
            />
          ) : isUploading ? (
            <div className="bg-card rounded-2xl shadow-card p-8">
              <UploadProgress
                progress={uploadProgress}
                isProcessing={uploadProgress > 50}
              />
            </div>
          ) : (
            <div className="bg-card rounded-2xl shadow-card p-6 md:p-8">
              <FileUploadZone
                onFileSelect={handleFileSelect}
                isUploading={isUploading}
                acceptedFile={selectedFile}
                onClear={handleClear}
              />

              {/* Error */}
              {error && (
                <div className="mt-6 p-4 bg-destructive/10 border border-destructive/20 rounded-xl flex gap-3">
                  <AlertCircle className="h-5 w-5 text-destructive mt-0.5" />
                  <div>
                    <p className="font-medium text-destructive">
                      Upload Failed
                    </p>
                    <p className="text-sm text-destructive/80">{error}</p>
                  </div>
                </div>
              )}

              {/* Upload Button */}
              {selectedFile && !isUploading && (
                <div className="mt-6 flex justify-center">
                  <Button
                    variant="hero"
                    size="lg"
                    onClick={handleUpload}
                    className="min-w-[200px]"
                  >
                    <Upload className="mr-2 h-5 w-5" />
                    Extract Invoice
                  </Button>
                </div>
              )}
            </div>
          )}

          {/* Footer Help */}
          {!data && !isUploading && (
            <div className="mt-8 text-center">
              <p className="text-sm text-muted-foreground">
                Supported format: <span className="font-medium">PDF</span>
              </p>
              <p className="text-sm text-muted-foreground mt-1">
                Maximum file size: <span className="font-medium">10 MB</span>
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default UploadPage;
