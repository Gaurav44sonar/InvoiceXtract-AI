import { useState, useEffect, useCallback } from 'react';
import { InvoiceHistoryItem } from '@/services/api';

// Mock data for demo purposes - replace with actual API calls when backend is ready
const mockHistory: InvoiceHistoryItem[] = [
  {
    id: '1',
    file_name: 'invoice_2024_001.pdf',
    upload_date: '2024-01-15T10:30:00Z',
    status: 'processed',
    data: {
      invoice_number: 'INV-2024-001',
      invoice_date: '2024-01-15',
      vendor_name: 'Tech Solutions Ltd.',
      gst_amount: 1800,
      total_amount: 11800,
      line_items: [
        { description: 'Web Development Services', quantity: 1, unit_price: 10000, amount: 10000 },
      ],
    },
  },
  {
    id: '2',
    file_name: 'vendor_bill_jan.png',
    upload_date: '2024-01-14T14:20:00Z',
    status: 'processed',
    data: {
      invoice_number: 'VB-2024-042',
      invoice_date: '2024-01-14',
      vendor_name: 'Office Supplies Co.',
      gst_amount: 540,
      total_amount: 3540,
      line_items: [
        { description: 'Printer Paper (Box)', quantity: 5, unit_price: 500, amount: 2500 },
        { description: 'Ink Cartridges', quantity: 2, unit_price: 270, amount: 540 },
      ],
    },
  },
  {
    id: '3',
    file_name: 'receipt_misc.jpg',
    upload_date: '2024-01-13T09:15:00Z',
    status: 'failed',
  },
];

interface UseInvoiceHistoryReturn {
  history: InvoiceHistoryItem[];
  isLoading: boolean;
  error: string | null;
  refetch: () => void;
  addToHistory: (item: InvoiceHistoryItem) => void;
}

export const useInvoiceHistory = (): UseInvoiceHistoryReturn => {
  const [history, setHistory] = useState<InvoiceHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Simulate API call - replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 500));
      
      // Load from localStorage or use mock data
      const stored = localStorage.getItem('invoiceHistory');
      if (stored) {
        setHistory(JSON.parse(stored));
      } else {
        setHistory(mockHistory);
        localStorage.setItem('invoiceHistory', JSON.stringify(mockHistory));
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch history');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const addToHistory = useCallback((item: InvoiceHistoryItem) => {
    setHistory((prev) => {
      const updated = [item, ...prev];
      localStorage.setItem('invoiceHistory', JSON.stringify(updated));
      return updated;
    });
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  return {
    history,
    isLoading,
    error,
    refetch: fetchHistory,
    addToHistory,
  };
};
