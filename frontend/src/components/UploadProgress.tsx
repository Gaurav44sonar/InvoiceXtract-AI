import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface UploadProgressProps {
  progress: number;
  isProcessing: boolean;
}

const UploadProgress = ({ progress, isProcessing }: UploadProgressProps) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 animate-fade-in">
      <div className="relative mb-6">
        <div className="w-24 h-24 rounded-full bg-secondary flex items-center justify-center">
          <Loader2 className="w-12 h-12 text-primary animate-spin" />
        </div>
        <svg className="absolute inset-0 w-24 h-24 -rotate-90">
          <circle
            cx="48"
            cy="48"
            r="44"
            fill="none"
            stroke="hsl(var(--border))"
            strokeWidth="8"
          />
          <circle
            cx="48"
            cy="48"
            r="44"
            fill="none"
            stroke="hsl(var(--primary))"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={`${2 * Math.PI * 44}`}
            strokeDashoffset={`${2 * Math.PI * 44 * (1 - progress / 100)}`}
            className="transition-all duration-300"
          />
        </svg>
      </div>
      
      <div className="text-center">
        <p className="text-2xl font-bold text-foreground mb-2">{progress}%</p>
        <p className="text-muted-foreground">
          {isProcessing ? 'Extracting invoice data...' : 'Uploading file...'}
        </p>
      </div>

      <div className="w-full max-w-xs mt-6">
        <div className="h-2 bg-secondary rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-hero transition-all duration-300 rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="mt-8 flex items-center gap-2 text-sm text-muted-foreground">
        <div className={cn(
          "w-2 h-2 rounded-full animate-pulse",
          progress < 50 ? "bg-warning" : progress < 100 ? "bg-primary" : "bg-success"
        )} />
        <span>
          {progress < 30 && "Uploading file to server..."}
          {progress >= 30 && progress < 60 && "Processing document..."}
          {progress >= 60 && progress < 90 && "Extracting data with AI..."}
          {progress >= 90 && "Finalizing results..."}
        </span>
      </div>
    </div>
  );
};

export default UploadProgress;
