import { API } from "@/lib/config";
import { API_ENDPOINTS } from "@/constants/config";
import {
  DetectionResponse,
  DetectionsListResponse,
} from "@/constants/types";

/**
 * Upload an image for tree detection
 * @param file - Image file to analyze
 * @returns Promise with detection results
 */
export const uploadImage = async (file: File): Promise<DetectionResponse> => {
  try {
    const formData = new FormData();
    formData.append("file", file);
    
    const response = await API.post<DetectionResponse>(
      API_ENDPOINTS.UPLOAD,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    
    return response.data;
  } catch (error) {
    console.error("Error uploading image:", error);
    throw error;
  }
};

/**
 * Fetch all detections from the backend
 * @param limit - Maximum number of records to fetch
 * @returns Promise with detections list
 */
export const fetchDetections = async (
  limit: number = 50
): Promise<DetectionsListResponse> => {
  try {
    const response = await API.get<DetectionsListResponse>(
      `${API_ENDPOINTS.DETECTIONS}?limit=${limit}`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching detections:", error);
    throw error;
  }
};

/**
 * Fetch a specific detection by ID
 * @param id - Detection ID
 * @returns Promise with detection data
 */
export const fetchDetectionById = async (id: string) => {
  try {
    const response = await API.get(API_ENDPOINTS.DETECTION_BY_ID(id));
    return response.data;
  } catch (error) {
    console.error("Error fetching detection:", error);
    throw error;
  }
};

/**
 * Check API health
 * @returns Promise with health status
 */
export const checkHealth = async () => {
  try {
    const response = await API.get(API_ENDPOINTS.HEALTH);
    return response.data;
  } catch (error) {
    console.error("Error checking health:", error);
    throw error;
  }
};
