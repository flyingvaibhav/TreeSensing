import { API } from "@/lib/config";
import { TreesApiResponse } from "@/constants/types";

/**
 * API Route handler for trees endpoint
 * This file can be used for Next.js API routes if needed
 */
export async function GET() {
  try {
    const response = await API.get<TreesApiResponse>("/trees");
    return Response.json(response.data);
  } catch (error) {
    console.error("Error fetching trees:", error);
    return Response.json(
      { error: "Failed to fetch trees" },
      { status: 500 }
    );
  }
}

