import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import Navbar from '@/components/Navbar';
import { 
  Upload, 
  FileText, 
  Database, 
  Zap, 
  Shield, 
  Clock,
  ArrowRight,
  CheckCircle2
} from 'lucide-react';

const Index = () => {
  const features = [
    {
      icon: Zap,
      title: 'AI-Powered Extraction',
      description: 'Advanced OCR technology extracts invoice data with high accuracy in seconds.',
    },
    {
      icon: Database,
      title: 'Instant Storage',
      description: 'All extracted data is automatically organized and stored for easy access.',
    },
    {
      icon: Shield,
      title: 'Secure Processing',
      description: 'Enterprise-grade security ensures your financial documents stay protected.',
    },
    {
      icon: Clock,
      title: 'Save Hours of Work',
      description: 'Automate manual data entry and reduce processing time by up to 90%.',
    },
  ];

  const steps = [
    { number: '01', title: 'Upload Invoice', description: 'Drag & drop or click to upload PDF or image files' },
    { number: '02', title: 'AI Processing', description: 'Our AI extracts all relevant invoice data automatically' },
    { number: '03', title: 'Review & Save', description: 'Verify the extracted data and save to your records' },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-primary/5 rounded-full blur-3xl translate-x-1/2 -translate-y-1/2" />
          <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-accent/5 rounded-full blur-3xl -translate-x-1/2 translate-y-1/2" />
        </div>

        <div className="container py-20 md:py-32">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full mb-6 animate-fade-in">
              <Zap className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium text-primary">Powered by Advanced AI</span>
            </div>
            
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6 animate-slide-up">
              <span className="text-gradient">InvoiceXtract</span>
              <span className="text-foreground"> AI</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto animate-slide-up" style={{ animationDelay: '0.1s' }}>
              Upload invoices. Extract data. Store results instantly.
              <br />
              <span className="text-foreground font-medium">Automate your invoice processing today.</span>
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <Button variant="hero" size="xl" asChild>
                <Link to="/upload">
                  <Upload className="mr-2 h-5 w-5" />
                  Upload Invoice
                </Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link to="/history">
                  View History
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>

            {/* Trust badges */}
            <div className="flex items-center justify-center gap-6 mt-12 text-sm text-muted-foreground animate-fade-in" style={{ animationDelay: '0.3s' }}>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-success" />
                <span>99% Accuracy</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-success" />
                <span>Secure & Private</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-success" />
                <span>Instant Results</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20 bg-card">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              How It Works
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Three simple steps to extract and organize your invoice data
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {steps.map((step, index) => (
              <div 
                key={step.number}
                className="relative p-6 bg-background rounded-2xl shadow-card hover:shadow-card-hover transition-all duration-300 group"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="text-6xl font-bold text-gradient opacity-20 mb-4">
                  {step.number}
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
                  {step.title}
                </h3>
                <p className="text-muted-foreground">
                  {step.description}
                </p>
                {index < steps.length - 1 && (
                  <ArrowRight className="hidden md:block absolute top-1/2 -right-6 h-6 w-6 text-border" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Why Choose InvoiceXtract?
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Built for businesses that want to streamline their invoice processing workflow
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={feature.title}
                  className="p-6 bg-card rounded-2xl shadow-card hover:shadow-card-hover hover:-translate-y-1 transition-all duration-300"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="w-12 h-12 rounded-xl bg-gradient-hero flex items-center justify-center mb-4">
                    <Icon className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <h3 className="text-lg font-semibold text-foreground mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container">
          <div className="relative bg-gradient-hero rounded-3xl p-8 md:p-16 overflow-hidden">
            <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMSIgZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjEpIi8+PC9zdmc+')] opacity-50" />
            
            <div className="relative text-center max-w-2xl mx-auto">
              <FileText className="h-16 w-16 text-primary-foreground/80 mx-auto mb-6" />
              <h2 className="text-3xl md:text-4xl font-bold text-primary-foreground mb-4">
                Ready to Get Started?
              </h2>
              <p className="text-lg text-primary-foreground/80 mb-8">
                Upload your first invoice and experience the power of AI-driven data extraction.
              </p>
              <Button 
                size="xl" 
                className="bg-card text-foreground hover:bg-card/90 shadow-xl"
                asChild
              >
                <Link to="/upload">
                  <Upload className="mr-2 h-5 w-5" />
                  Upload Your First Invoice
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-border">
        <div className="container">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-hero">
                <FileText className="h-4 w-4 text-primary-foreground" />
              </div>
              <span className="font-bold text-gradient">InvoiceXtract AI</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2024 InvoiceXtract. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
