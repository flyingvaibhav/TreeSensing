"use client";

import { useEffect, useState } from "react";
import { fetchDetections } from "@/utils/api";
import { Detection } from "@/constants/types";
import Link from "next/link";

export default function DetectionsPage() {
  const [detections, setDetections] = useState<Detection[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadDetections = async () => {
      try {
        setLoading(true);
        const response = await fetchDetections(50);
        setDetections(response.data);
      } catch (err) {
        setError("Failed to load detections");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadDetections();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold mb-4">🌳 Detection History</h1>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold mb-4">🌳 Detection History</h1>
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  const totalTrees = detections.reduce((sum, d) => sum + d.tree_count, 0);
  const avgConfidence =
    detections.length > 0
      ? detections.reduce((sum, d) => sum + d.avg_confidence, 0) /
        detections.length
      : 0;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold mb-2">🌳 Detection History</h1>
            <p className="text-gray-600">
              View all tree detection results from uploaded images
            </p>
          </div>
          <Link
            href="/upload"
            className="px-6 py-3 bg-green-600 text-white rounded-lg
              hover:bg-green-700 transition-colors font-medium"
          >
            + New Detection
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600 mb-1">Total Detections</p>
            <p className="text-3xl font-bold text-gray-900">
              {detections.length}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600 mb-1">Total Trees Detected</p>
            <p className="text-3xl font-bold text-green-600">{totalTrees}</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600 mb-1">Avg. Confidence</p>
            <p className="text-3xl font-bold text-blue-600">
              {(avgConfidence * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        {/* Detection List */}
        {detections.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-500 mb-4">No detections found</p>
            <Link
              href="/upload"
              className="inline-block px-6 py-3 bg-green-600 text-white rounded-lg
                hover:bg-green-700 transition-colors font-medium"
            >
              Upload First Image
            </Link>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Filename
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Trees
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Confidence
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Image Size
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {detections.map((detection, index) => (
                  <tr key={detection.id || index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {detection.filename}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        {detection.tree_count}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {(detection.avg_confidence * 100).toFixed(1)}%
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">
                        {detection.image_size.width} × {detection.image_size.height}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">
                        {new Date(detection.timestamp).toLocaleDateString()}
                      </div>
                      <div className="text-xs text-gray-400">
                        {new Date(detection.timestamp).toLocaleTimeString()}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
