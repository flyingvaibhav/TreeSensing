"use client";

import { useState } from "react";
import { uploadImage } from "@/utils/api";
import { Detection } from "@/constants/types";
import { APP_CONFIG } from "@/constants/config";

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Detection | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file size
    if (file.size > APP_CONFIG.MAX_FILE_SIZE) {
      setError("File size exceeds 10MB limit");
      return;
    }

    // Validate file type
    const allowedTypes = APP_CONFIG.ALLOWED_FILE_TYPES as readonly string[];
    if (!allowedTypes.includes(file.type)) {
      setError("Please select a valid image file (JPEG, JPG, PNG)");
      return;
    }

    setSelectedFile(file);
    setError(null);
    setResult(null);

    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const response = await uploadImage(selectedFile);
      setResult(response.data);
    } catch (err) {
      setError("Failed to process image. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">🌳 Tree Detection</h1>
        <p className="text-gray-600 mb-8">
          Upload an aerial image to detect and count trees
        </p>

        {/* Upload Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="mb-4">
            <label
              htmlFor="file-upload"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Select Image
            </label>
            <input
              id="file-upload"
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-md file:border-0
                file:text-sm file:font-semibold
                file:bg-green-50 file:text-green-700
                hover:file:bg-green-100
                cursor-pointer"
            />
            <p className="text-xs text-gray-500 mt-1">
              Max file size: 10MB. Supported: JPEG, JPG, PNG
            </p>
          </div>

          {/* Preview */}
          {preview && (
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Preview:</p>
              <img
                src={preview}
                alt="Preview"
                className="max-w-full h-auto rounded-lg border border-gray-300"
                style={{ maxHeight: "400px" }}
              />
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button
              onClick={handleUpload}
              disabled={!selectedFile || loading}
              className="px-6 py-2 bg-green-600 text-white rounded-md
                hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed
                transition-colors font-medium"
            >
              {loading ? "Processing..." : "Detect Trees"}
            </button>
            {(selectedFile || result) && (
              <button
                onClick={handleReset}
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded-md
                  hover:bg-gray-300 transition-colors font-medium"
              >
                Reset
              </button>
            )}
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 text-green-700">
              ✅ Detection Complete
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="p-4 bg-green-50 rounded-lg">
                <p className="text-sm text-gray-600">Trees Detected</p>
                <p className="text-3xl font-bold text-green-700">
                  {result.tree_count}
                </p>
              </div>

              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-600">Avg. Confidence</p>
                <p className="text-3xl font-bold text-blue-700">
                  {(result.avg_confidence * 100).toFixed(1)}%
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <p className="text-sm font-medium text-gray-700">Filename:</p>
                <p className="text-gray-900">{result.filename}</p>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700">Image Size:</p>
                <p className="text-gray-900">
                  {result.image_size.width} × {result.image_size.height} px
                </p>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700">Processed At:</p>
                <p className="text-gray-900">
                  {new Date(result.timestamp).toLocaleString()}
                </p>
              </div>

              {result.confidences.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-1">
                    Individual Confidence Scores:
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {result.confidences.slice(0, 10).map((conf, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-gray-100 rounded text-xs"
                      >
                        {(conf * 100).toFixed(1)}%
                      </span>
                    ))}
                    {result.confidences.length > 10 && (
                      <span className="px-2 py-1 text-xs text-gray-500">
                        +{result.confidences.length - 10} more
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
