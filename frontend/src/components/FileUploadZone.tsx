import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, Image, X, CheckCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface FileUploadZoneProps {
  onFileSelect: (file: File) => void;
  isUploading: boolean;
  acceptedFile: File | null;
  onClear: () => void;
}

const FileUploadZone = ({ onFileSelect, isUploading, acceptedFile, onClear }: FileUploadZoneProps) => {
  const [preview, setPreview] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      onFileSelect(file);
      
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = () => setPreview(reader.result as string);
        reader.readAsDataURL(file);
      } else {
        setPreview(null);
      }
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
    },
    maxFiles: 1,
    disabled: isUploading,
  });

  const handleClear = (e: React.MouseEvent) => {
    e.stopPropagation();
    setPreview(null);
    onClear();
  };

  const getFileIcon = (file: File) => {
    if (file.type === 'application/pdf') {
      return <FileText className="h-16 w-16 text-destructive" />;
    }
    return <Image className="h-16 w-16 text-accent" />;
  };

  return (
    <div
      {...getRootProps()}
      className={cn(
        "relative flex flex-col items-center justify-center w-full min-h-[320px] p-8 border-2 border-dashed rounded-2xl cursor-pointer transition-all duration-300",
        isDragActive && !isDragReject && "border-primary bg-primary/5 scale-[1.02]",
        isDragReject && "border-destructive bg-destructive/5",
        !isDragActive && !acceptedFile && "border-border hover:border-primary/50 hover:bg-secondary/50",
        acceptedFile && "border-success bg-success/5",
        isUploading && "pointer-events-none opacity-60"
      )}
    >
      <input {...getInputProps()} />
      
      {acceptedFile ? (
        <div className="flex flex-col items-center gap-4 animate-scale-in">
          <div className="relative">
            {preview ? (
              <img 
                src={preview} 
                alt="Preview" 
                className="w-32 h-32 object-cover rounded-xl shadow-lg"
              />
            ) : (
              <div className="flex items-center justify-center w-32 h-32 bg-card rounded-xl shadow-lg">
                {getFileIcon(acceptedFile)}
              </div>
            )}
            <button
              onClick={handleClear}
              className="absolute -top-2 -right-2 p-1 bg-destructive text-destructive-foreground rounded-full shadow-md hover:bg-destructive/90 transition-colors"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
          <div className="text-center">
            <p className="font-medium text-foreground">{acceptedFile.name}</p>
            <p className="text-sm text-muted-foreground">
              {(acceptedFile.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
          <div className="flex items-center gap-2 text-success">
            <CheckCircle className="h-5 w-5" />
            <span className="text-sm font-medium">Ready to upload</span>
          </div>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-4 text-center">
          <div className={cn(
            "p-6 rounded-full transition-all duration-300",
            isDragActive ? "bg-primary/10" : "bg-secondary"
          )}>
            <Upload className={cn(
              "h-12 w-12 transition-all duration-300",
              isDragActive ? "text-primary scale-110" : "text-muted-foreground"
            )} />
          </div>
          <div>
            <p className="text-lg font-medium text-foreground">
              {isDragActive ? "Drop your invoice here" : "Drag & drop your invoice"}
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              or click to browse files
            </p>
          </div>
          <div className="flex items-center gap-3 mt-2">
            <div className="flex items-center gap-1.5 px-3 py-1.5 bg-card rounded-full shadow-sm">
              <FileText className="h-4 w-4 text-destructive" />
              <span className="text-xs font-medium">PDF</span>
            </div>
            <div className="flex items-center gap-1.5 px-3 py-1.5 bg-card rounded-full shadow-sm">
              <Image className="h-4 w-4 text-accent" />
              <span className="text-xs font-medium">JPG / PNG</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUploadZone;
