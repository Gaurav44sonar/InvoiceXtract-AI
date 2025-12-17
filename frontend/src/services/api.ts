import axios from "axios";

/**
 * Backend base URL
 */
const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Axios instance
 */
const api = axios.create({
  baseURL: API_BASE_URL,
});

/**
 * Types (match backend response)
 */
export interface LineItem {
  description: string;
  quantity: number | string;
  unit_price: number | string;
  total: number | string;
}

export interface ExtractedInvoiceData {
  invoice_number: string;
  invoice_date: string;
  vendor?: {
    name?: string;
    address?: string;
  };
  customer?: {
    name?: string;
  };
  items: LineItem[];
  gst_amount?: number | string;
  total_amount?: number | string;
}

/**
 * Upload invoice → call FastAPI backend
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

export default api;
