import { useState, useCallback } from "react";
import { uploadInvoice, ExtractedInvoiceData } from "@/services/api";

interface UseInvoiceUploadReturn {
  isUploading: boolean;
  uploadProgress: number;
  error: string | null;
  data: ExtractedInvoiceData | null;
  upload: (file: File) => Promise<ExtractedInvoiceData>;
  reset: () => void;
}

export const useInvoiceUpload = (): UseInvoiceUploadReturn => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<ExtractedInvoiceData | null>(null);

  const upload = useCallback(async (file: File) => {
    setIsUploading(true);
    setError(null);
    setUploadProgress(5);

    // Fake progress for UX
    const interval = setInterval(() => {
      setUploadProgress((p) => (p < 90 ? p + 10 : p));
    }, 200);

    try {
      const result = await uploadInvoice(file);
      clearInterval(interval);

      setUploadProgress(100);
      setData(result);

      return result;
    } catch (err: any) {
      clearInterval(interval);
      setError(err?.message || "Invoice upload failed");
      setUploadProgress(0);
      throw err;
    } finally {
      setIsUploading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setIsUploading(false);
    setUploadProgress(0);
    setError(null);
    setData(null);
  }, []);

  return {
    isUploading,
    uploadProgress,
    error,
    data,
    upload,
    reset,
  };
};
