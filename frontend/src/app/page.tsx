import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🌳 TreeSense Imaging
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            AI-Powered Tree Detection & Counting
          </p>
          <p className="text-gray-500">
            Upload aerial images and let our ML model detect and count trees automatically
          </p>
        </div>

        {/* Action Cards */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <Link href="/upload">
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow cursor-pointer border-2 border-transparent hover:border-green-500">
              <div className="text-4xl mb-4">📤</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-3">
                Upload & Detect
              </h2>
              <p className="text-gray-600 mb-4">
                Upload an aerial image and get instant tree detection results with confidence scores
              </p>
              <span className="text-green-600 font-semibold">
                Start Detection →
              </span>
            </div>
          </Link>

          <Link href="/trees">
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow cursor-pointer border-2 border-transparent hover:border-blue-500">
              <div className="text-4xl mb-4">📊</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-3">
                View History
              </h2>
              <p className="text-gray-600 mb-4">
                Browse all previous detection results and analyze trends in your tree data
              </p>
              <span className="text-blue-600 font-semibold">
                View Results →
              </span>
            </div>
          </Link>
        </div>

        {/* Features */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            Features
          </h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl mb-3">🎯</div>
              <h4 className="font-semibold text-gray-900 mb-2">
                High Accuracy
              </h4>
              <p className="text-sm text-gray-600">
                YOLOv8-powered detection with confidence scoring
              </p>
            </div>

            <div className="text-center">
              <div className="text-3xl mb-3">⚡</div>
              <h4 className="font-semibold text-gray-900 mb-2">
                Fast Processing
              </h4>
              <p className="text-sm text-gray-600">
                Get results in seconds with optimized ML pipeline
              </p>
            </div>

            <div className="text-center">
              <div className="text-3xl mb-3">💾</div>
              <h4 className="font-semibold text-gray-900 mb-2">
                Data Storage
              </h4>
              <p className="text-sm text-gray-600">
                All results stored in MongoDB for future analysis
              </p>
            </div>
          </div>
        </div>

        {/* Tech Stack */}
        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500 mb-3">Powered by</p>
          <div className="flex justify-center gap-6 flex-wrap">
            <span className="px-4 py-2 bg-white rounded-full shadow text-sm font-medium">
              Next.js
            </span>
            <span className="px-4 py-2 bg-white rounded-full shadow text-sm font-medium">
              FastAPI
            </span>
            <span className="px-4 py-2 bg-white rounded-full shadow text-sm font-medium">
              YOLOv8
            </span>
            <span className="px-4 py-2 bg-white rounded-full shadow text-sm font-medium">
              MongoDB
            </span>
            <span className="px-4 py-2 bg-white rounded-full shadow text-sm font-medium">
              Python
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
