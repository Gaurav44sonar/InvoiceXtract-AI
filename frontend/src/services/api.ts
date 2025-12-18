import axios from "axios";

/**
 * Change this if backend URL changes
 * Local FastAPI default: http://127.0.0.1:8000
 */
const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
});

/* ----------------------------------
   Types
---------------------------------- */

export interface InvoiceItem {
  description: string;
  quantity: number;
  unit_price?: number;
  total?: number;
}

export interface ExtractedInvoiceData {
  invoice_number: string;
  invoice_date: string;
  vendor?: {
    name?: string;
    address?: string;
  };
  subtotal?: number;
  tax_amount?: number;
  total?: number;
  currency?: string;
  items: InvoiceItem[];
}

export interface InvoiceHistoryItem {
  id: string;
  file_name: string;
  invoice_number: string;
  invoice_date: string;
  vendor_name: string;
  subtotal?: number;
  tax_amount?: number;
  total?: number;
  currency?: string;
  items: InvoiceItem[];
  created_at: string;
}

/* ----------------------------------
   API Calls
---------------------------------- */

/**
 * 1️⃣ Upload & Extract Invoice (NO SAVE)
 */
export const uploadInvoice = async (
  file: File
): Promise<ExtractedInvoiceData> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/extract-invoice", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

/**
 * 2️⃣ Save Extracted Invoice to MongoDB
 */
export const saveInvoice = async (
  fileName: string,
  data: ExtractedInvoiceData
) => {
  const payload = {
    file_name: fileName,
    ...data,
  };

  const response = await api.post("/save-invoice", payload);
  return response.data;
};

/**
 * 3️⃣ Fetch Invoice History
 */
export const getInvoiceHistory = async (): Promise<InvoiceHistoryItem[]> => {
  const response = await api.get("/invoices");
  return response.data;
};

/**
 * 4️⃣ Fetch Single Invoice
 */
export const getInvoiceById = async (
  id: string
): Promise<InvoiceHistoryItem> => {
  const response = await api.get(`/invoices/${id}`);
  return response.data;
};

export default api;
