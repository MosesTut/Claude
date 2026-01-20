import axios from 'axios';
import { API_CONFIG } from '../config/api';

/**
 * Health Check Utility
 * Verifies backend API is reachable before attempting authentication
 */

export interface HealthCheckResult {
  isHealthy: boolean;
  status?: string;
  database?: string;
  error?: string;
  latency?: number;
}

/**
 * Check if backend API is reachable and healthy
 *
 * @returns Promise<HealthCheckResult>
 */
export async function checkBackendHealth(): Promise<HealthCheckResult> {
  const startTime = Date.now();

  try {
    const response = await axios.get(`${API_CONFIG.BASE_URL}/health`, {
      timeout: 5000, // 5 second timeout
    });

    const latency = Date.now() - startTime;

    if (response.status === 200 && response.data.status === 'healthy') {
      return {
        isHealthy: true,
        status: response.data.status,
        database: response.data.database,
        latency,
      };
    } else {
      return {
        isHealthy: false,
        error: 'Backend returned unhealthy status',
        latency,
      };
    }
  } catch (error: any) {
    const latency = Date.now() - startTime;

    if (error.code === 'ECONNREFUSED') {
      return {
        isHealthy: false,
        error: 'Cannot connect to backend. Make sure the server is running.',
        latency,
      };
    } else if (error.code === 'ETIMEDOUT' || error.code === 'ECONNABORTED') {
      return {
        isHealthy: false,
        error: 'Backend is not responding. Server may be overloaded.',
        latency,
      };
    } else {
      return {
        isHealthy: false,
        error: error.message || 'Unknown error connecting to backend',
        latency,
      };
    }
  }
}

/**
 * Display health check result in user-friendly format
 */
export function formatHealthCheckResult(result: HealthCheckResult): string {
  if (result.isHealthy) {
    return `✅ Backend is healthy (${result.latency}ms)\nDatabase: ${result.database}`;
  } else {
    return `❌ Backend health check failed\n${result.error}\nLatency: ${result.latency}ms`;
  }
}
