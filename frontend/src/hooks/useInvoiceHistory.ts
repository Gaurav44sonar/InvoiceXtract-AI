import { useState, useEffect, useCallback } from "react";
import {
  getInvoiceHistory,
  saveInvoice,
  InvoiceHistoryItem,
  ExtractedInvoiceData,
} from "@/services/api";

interface UseInvoiceHistoryReturn {
  history: InvoiceHistoryItem[];
  isLoading: boolean;
  error: string | null;
  saveToHistory: (fileName: string, data: ExtractedInvoiceData) => Promise<void>;
  refetch: () => Promise<void>;
}

export const useInvoiceHistory = (): UseInvoiceHistoryReturn => {
  const [history, setHistory] = useState<InvoiceHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch history from MongoDB
   */
  const fetchHistory = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await getInvoiceHistory();
      setHistory(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load invoice history");
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Save invoice to MongoDB
   */
  const saveToHistory = useCallback(
    async (fileName: string, data: ExtractedInvoiceData) => {
      try {
        await saveInvoice(fileName, data);
        await fetchHistory(); // refresh history after save
      } catch (err: any) {
        throw new Error(err?.message || "Failed to save invoice");
      }
    },
    [fetchHistory]
  );

  /**
   * Load history on page load
   */
  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  return {
    history,
    isLoading,
    error,
    saveToHistory,
    refetch: fetchHistory,
  };
};
