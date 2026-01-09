import React, { useState, useEffect } from "react";
import apiClient from "../api/client";
import toast from "react-hot-toast";
import {
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Target,
  Zap,
  Calendar,
  Download,
  FileText,
  Loader2,
  BarChart3,
  Pencil,
  Image as ImageIcon,
  Heart,
  TrendingDown,
  Bot,
  Goal
} from "lucide-react";

export default function WeeklyReportsPage() {
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);

  useEffect(() => {
    fetchWeeklyReport();
  }, []);

  const fetchWeeklyReport = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get("/reports/weekly/");
      setReport(response.data);
    } catch (error) {
      console.error("Error fetching report:", error);
      toast.error("Failed to load weekly report");
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportPDF = async () => {
    setIsGeneratingPDF(true);
    let toastId;

    try {
      // Show loading toast
      toastId = toast.loading(
        <div className="flex items-center gap-2">
          <Loader2 className="w-4 h-4 animate-spin" />
          <span>Generating PDF report...</span>
        </div>,
        { duration: Infinity }
      );

      // Request PDF with proper config
      const response = await apiClient.post(
        "/reports/weekly/pdf/",
        {},
        {
          responseType: 'blob', // CRITICAL: Tell axios to expect binary data
          timeout: 60000, // 60 second timeout
          headers: {
            'Accept': 'application/pdf',
          },
        }
      );

      // Check if response is actually a PDF
      if (response.data.type !== 'application/pdf') {
        throw new Error('Invalid response type. Expected PDF.');
      }

      // Create blob with explicit type
      const blob = new Blob([response.data], {
        type: 'application/pdf'
      });

      // Verify blob size
      if (blob.size === 0) {
        throw new Error('Generated PDF is empty');
      }

      console.log(`PDF generated: ${blob.size} bytes`);

      // Create download URL
      const url = window.URL.createObjectURL(blob);

      // Create link and trigger download
      const link = document.createElement('a');
      link.href = url;
      link.download = `advision_weekly_report_${new Date().toISOString().split('T')[0]}.pdf`;
      link.style.display = 'none';

      document.body.appendChild(link);
      link.click();

      // Cleanup
      setTimeout(() => {
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      }, 100);

      // Success feedback
      toast.success(
        <div className="flex items-center gap-2">
          <CheckCircle className="w-4 h-4" />
          <span>PDF downloaded successfully!</span>
        </div>,
        { id: toastId, duration: 3000 }
      );

    } catch (error) {
      console.error("PDF Generation Error:", error);

      let errorMessage = "Failed to generate PDF report";

      if (error.response) {
        // Server responded with error
        if (error.response.status === 500) {
          errorMessage = "Server error. Please check if ReportLab is installed.";
        } else if (error.response.status === 401) {
          errorMessage = "Please log in again to generate report.";
        } else if (error.response.data?.error) {
          errorMessage = error.response.data.error;
        }
      } else if (error.request) {
        // Request made but no response
        errorMessage = "No response from server. Please check your connection.";
      } else if (error.message) {
        errorMessage = error.message;
      }

      toast.error(
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          <span>{errorMessage}</span>
        </div>,
        { id: toastId, duration: 5000 }
      );
    } finally {
      setIsGeneratingPDF(false);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'border-red-500 bg-red-500/10';
      case 'medium':
        return 'border-yellow-500 bg-yellow-500/10';
      case 'low':
        return 'border-green-500 bg-green-500/10';
      default:
        return 'border-gray-500 bg-gray-500/10';
    }
  };

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-500/20 text-red-300';
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-300';
      case 'low':
        return 'bg-green-500/20 text-green-300';
      default:
        return 'bg-gray-500/20 text-gray-300';
    }
  };

  const getCategoryIcon = (category) => {
    switch (category.toLowerCase()) {
      case 'performance':
        return <TrendingUp className="w-4 h-4" />;
      case 'growth':
        return <Zap className="w-4 h-4" />;
      case 'engagement':
        return <Target className="w-4 h-4" />;
      case 'budget':
        return <AlertTriangle className="w-4 h-4" />;
      default:
        return <CheckCircle className="w-4 h-4" />;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#0f0c12] via-[#16111d] to-[#0d0b11] text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-[#a88fd8] border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-400">Loading weekly report...</p>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#0f0c12] via-[#16111d] to-[#0d0b11] text-white flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">No Report Available</h2>
          <p className="text-gray-400">Weekly report could not be loaded</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-4 md:px-6 py-10 bg-gradient-to-br from-[#0f0c12] via-[#16111d] to-[#0d0b11] text-white">

      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-10">
        <div>
          <h1 className="text-2xl md:text-3xl font-semibold tracking-wide flex items-center gap-2">
            <Calendar className="w-7 h-7 text-[#a88fd8]" />
            Weekly Performance Report
          </h1>
          <p className="text-gray-400 text-sm mt-1">{report.period}</p>
        </div>

        <button
          className={`px-5 py-2.5 bg-gradient-to-r from-[#3a3440] to-[#a88fd8] rounded-lg 
          hover:brightness-110 transition-all flex items-center gap-2 text-sm font-medium shadow-lg
          ${isGeneratingPDF ? 'opacity-70 cursor-not-allowed scale-95' : 'hover:scale-105'}`}
          onClick={handleExportPDF}
          disabled={isGeneratingPDF}
        >
          {isGeneratingPDF ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Generating PDF...</span>
            </>
          ) : (
            <>
              <Download className="w-4 h-4" />
              <span>Export PDF</span>
            </>
          )}
        </button>
      </div>

      {/* PDF Generation Overlay */}
      {isGeneratingPDF && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-[#1a1625] border border-[#a88fd8]/30 rounded-2xl p-8 max-w-md mx-4 shadow-2xl">
            <div className="flex flex-col items-center gap-4">
              <div className="relative">
                <div className="animate-spin h-16 w-16 border-4 border-[#a88fd8] border-t-transparent rounded-full"></div>
                <FileText className="w-6 h-6 text-[#a88fd8] absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
              </div>
              <div className="text-center">
                <h3 className="text-xl font-semibold text-white mb-2">
                  Generating Your Report
                </h3>
                <p className="text-gray-400 text-sm">
                  Please wait while we compile your weekly analytics...
                </p>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-1.5 overflow-hidden">
                <div className="bg-gradient-to-r from-[#a88fd8] to-[#6b5b95] h-full animate-pulse"></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 mb-10">
        {[
          {
            label: "Campaigns",
            value: report.summary.campaigns_created,
            change: null,
            icon: <BarChart3 className="w-5 h-5 text-white" />,
            color: "from-blue-500 to-blue-600"
          },
          {
            label: "Ads Generated",
            value: report.summary.ads_generated,
            change: null,
            icon: <Pencil className="w-5 h-5 text-white" />,
            color: "from-purple-500 to-purple-600"
          },
          {
            label: "Images",
            value: report.summary.images_generated,
            change: null,
            icon: <ImageIcon className="w-5 h-5 text-white" />,
            color: "from-pink-500 to-pink-600"
          },
          {
            label: "Active",
            value: report.summary.active_campaigns,
            change: null,
            icon: <Zap className="w-5 h-5 text-white" />,
            color: "from-green-500 to-green-600"
          },
          {
            label: "Engagement",
            value: report.summary.total_engagement?.toLocaleString() || 0,
            change: report.summary.engagement_growth,
            icon: <Heart className="w-5 h-5 text-white" />,
            color: "from-red-500 to-red-600"
          },
          {
            label: "Growth",
            value: report.summary.engagement_growth,
            change: null,
            icon: report.summary.engagement_growth?.includes('+')
              ? <TrendingUp className="w-5 h-5 text-white" />
              : <TrendingDown className="w-5 h-5 text-white" />,
            color: report.summary.engagement_growth?.includes('+')
              ? "from-green-500 to-green-600"
              : "from-orange-500 to-orange-600"
          },
        ].map((stat, i) => (
          <div
            key={i}
            className={`p-4 rounded-xl bg-gradient-to-br ${stat.color} shadow-lg hover:shadow-2xl transition-all duration-300`}
          >
            <div className="flex items-center justify-between mb-1">
              {/* Icon Bubble */}
              <div className="p-2 bg-white/20 rounded-full backdrop-blur-sm">
                {stat.icon}
              </div>

              {stat.change && (
                <span className={`text-xs px-2 py-0.5 rounded-full ${stat.change.includes('+') ? 'bg-white/20' : 'bg-black/20'
                  }`}>
                  {stat.change}
                </span>
              )}
            </div>

            <p className="text-xs opacity-80">{stat.label}</p>
            <p className="text-xl font-bold mt-0.5">{stat.value}</p>
          </div>
        ))}
      </div>


      {/* Key Insights */}
      <div className="p-6 rounded-xl mb-10 bg-black/30 border border-white/10 backdrop-blur-lg">
        <h2 className="text-xl font-semibold text-[#a88fd8] mb-6 flex items-center gap-2">
          <BarChart3 className="w-6 h-6 text-[#a88fd8]" />
          Key Insights
        </h2>


        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="p-4 bg-black/40 border border-white/5 rounded-lg">
            <p className="text-sm text-gray-400 mb-1">Top Platform</p>
            <p className="text-2xl font-bold text-[#a88fd8]">{report.insights.top_performing_platform}</p>
            <p className="text-xs text-gray-500 mt-1">Best performing channel</p>
          </div>

          <div className="p-4 bg-black/40 border border-white/5 rounded-lg">
            <p className="text-sm text-gray-400 mb-1">Top Campaign</p>
            {report.insights.top_campaign_name !== 'N/A' ? (
              <>
                <p className="text-lg font-bold text-green-400 truncate" title={report.insights.top_campaign_name}>
                  {report.insights.top_campaign_name}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Score: {report.insights.top_campaign_score}/100
                </p>
              </>
            ) : (
              <>
                <p className="text-lg font-bold text-gray-500">No campaigns yet</p>
                <p className="text-xs text-gray-500 mt-1">Create campaigns to see top performers</p>
              </>
            )}
          </div>

          <div className="p-4 bg-black/40 border border-white/5 rounded-lg">
            <p className="text-sm text-gray-400 mb-1">Average CTR</p>
            <p className="text-2xl font-bold text-blue-400">{report.insights.avg_ctr}%</p>
            <div className="flex items-center gap-1 mt-1">
              {report.insights.avg_ctr >= 5 ? (
                <span className="text-xs text-green-400">🔥 Excellent</span>
              ) : report.insights.avg_ctr >= 3 ? (
                <span className="text-xs text-blue-400">✅ Good</span>
              ) : (
                <span className="text-xs text-yellow-400">⚠️ Needs work</span>
              )}
            </div>
          </div>

          <div className="p-4 bg-black/40 border border-white/5 rounded-lg">
            <p className="text-sm text-gray-400 mb-1">Total Impressions</p>
            <p className="text-2xl font-bold text-purple-400">{report.insights.total_impressions?.toLocaleString() || 0}</p>
            <p className="text-xs text-gray-500 mt-1">{report.insights.impression_growth}</p>
          </div>

          <div className="p-4 bg-black/40 border border-white/5 rounded-lg">
            <p className="text-sm text-gray-400 mb-1">Total Conversions</p>
            <p className="text-2xl font-bold text-green-400">{report.insights.total_conversions?.toLocaleString() || 0}</p>
            <p className="text-xs text-gray-500 mt-1">{report.insights.conversion_growth}</p>
          </div>

          {report.insights.roas > 0 && (
            <div className="p-4 bg-black/40 border border-white/5 rounded-lg">
              <p className="text-sm text-gray-400 mb-1">ROAS</p>
              <p className="text-2xl font-bold text-yellow-400">{report.insights.roas}x</p>
              <p className="text-xs text-gray-500 mt-1">Return on ad spend</p>
            </div>
          )}
        </div>
      </div>

      {/* AI Recommendations - keeping existing code */}
      {report.recommendations && report.recommendations.length > 0 && (
        <div className="p-6 rounded-xl mb-10 bg-black/30 border border-white/10 backdrop-blur-lg">
          <h2 className="text-xl font-semibold text-[#a88fd8] mb-6 flex items-center gap-2">
            <Bot className="w-7 h-7 text-[#a88fd8]" />
            AI-Powered Recommendations
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {report.recommendations.map((rec, index) => (
              <div
                key={index}
                className={`p-5 rounded-xl border-l-4 ${getPriorityColor(rec.priority)} hover:shadow-lg transition-all`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className={`p-2 rounded-lg ${getPriorityBadge(rec.priority)}`}>
                      {getCategoryIcon(rec.category)}
                    </span>
                    <span className={`px-2 py-1 text-xs rounded-full ${getPriorityBadge(rec.priority)}`}>
                      {rec.priority.toUpperCase()}
                    </span>
                  </div>
                  {rec.impact && (
                    <span className="text-xs text-[#a88fd8] bg-[#a88fd8]/10 px-2 py-1 rounded-full">
                      {rec.impact}
                    </span>
                  )}
                </div>
                <h3 className="font-bold text-gray-100 mb-2">{rec.title}</h3>
                <p className="text-sm text-gray-300 leading-relaxed mb-3">{rec.description}</p>
                {rec.metric && (
                  <div className="flex items-center justify-between text-xs text-gray-400 mb-3 p-2 bg-black/30 rounded">
                    <div>
                      <span className="text-gray-500">Current:</span>
                      <span className="ml-1 text-gray-300">{rec.current}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Target:</span>
                      <span className="ml-1 text-[#a88fd8]">{rec.target}</span>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Next Steps */}
      {report.next_steps && report.next_steps.length > 0 && (
        <div className="p-6 rounded-xl bg-black/30 border border-white/10 backdrop-blur-lg">
          <h2 className="text-xl font-semibold text-[#a88fd8] mb-6 flex items-center gap-2">
            <Goal className="w-7 h-7 text-[#a88fd8]" />
            Next Steps
          </h2>

          <div className="space-y-3">
            {report.next_steps.map((step, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-4 bg-black/40 border border-white/5 
                rounded-lg hover:border-[#a88fd8]/30 transition-colors group"
              >
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[#a88fd8]/20 
                  flex items-center justify-center text-[#a88fd8] font-bold text-sm
                  group-hover:bg-[#a88fd8]/30 transition-colors">
                  {index + 1}
                </div>
                <p className="text-gray-200 leading-relaxed flex-1">{step}</p>
                <CheckCircle className="w-5 h-5 text-gray-600 group-hover:text-[#a88fd8] transition-colors flex-shrink-0" />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}