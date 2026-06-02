/**
 * API client for Stories of Stories backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

interface ApiResponse<T> {
  status: string;
  data?: T;
  message?: string;
  error?: string;
}

interface Node {
  id: number;
  title: string;
  content: string;
  choices: Choice[];
  metadata?: Record<string, unknown>;
}

interface Choice {
  id: number;
  text: string;
  nextNodeId: number;
  consequence?: string;
}

interface Story {
  id: number;
  title: string;
  description: string;
  author: string;
  published: boolean;
}

interface User {
  id: number;
  username: string;
  email: string;
}

/**
 * Generic API request handler
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    const data: ApiResponse<T> = await response.json();
    return data;
  } catch (error) {
    console.error('API Request Error:', error);
    return {
      status: 'error',
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

/**
 * Node API methods
 */
export const nodeAPI = {
  /**
   * Get all story nodes
   */
  async getAllNodes(): Promise<Node[]> {
    const response = await apiRequest<Node[]>('/nodes');
    return response.data || [];
  },

  /**
   * Get a specific node by ID
   */
  async getNode(nodeId: number): Promise<Node | null> {
    const response = await apiRequest<Node>(`/nodes/${nodeId}`);
    return response.data || null;
  },

  /**
   * Create a new node
   */
  async createNode(title: string, content: string): Promise<Node | null> {
    const response = await apiRequest<Node>('/nodes', {
      method: 'POST',
      body: JSON.stringify({ title, content }),
    });
    return response.data || null;
  },

  /**
   * Update a node
   */
  async updateNode(
    nodeId: number,
    title: string,
    content: string
  ): Promise<Node | null> {
    const response = await apiRequest<Node>(`/nodes/${nodeId}`, {
      method: 'PUT',
      body: JSON.stringify({ title, content }),
    });
    return response.data || null;
  },

  /**
   * Get choices for a node
   */
  async getNodeChoices(nodeId: number): Promise<Choice[]> {
    const response = await apiRequest<Choice[]>(`/nodes/${nodeId}/choices`);
    return response.data || [];
  },
};

/**
 * Choice API methods
 */
export const choiceAPI = {
  /**
   * Get all choices
   */
  async getAllChoices(): Promise<Choice[]> {
    const response = await apiRequest<Choice[]>('/choices');
    return response.data || [];
  },

  /**
   * Get a specific choice
   */
  async getChoice(choiceId: number): Promise<Choice | null> {
    const response = await apiRequest<Choice>(`/choices/${choiceId}`);
    return response.data || null;
  },

  /**
   * Make a choice (navigate to next node)
   */
  async makeChoice(
    choiceId: number,
    userId: number
  ): Promise<{ nextNode: Node; consequences: unknown[] } | null> {
    const response = await apiRequest<{
      nextNode: Node;
      consequences: unknown[];
    }>(`/choices/${choiceId}/make`, {
      method: 'POST',
      body: JSON.stringify({ userId }),
    });
    return response.data || null;
  },

  /**
   * Create a new choice
   */
  async createChoice(
    text: string,
    nextNodeId: number
  ): Promise<Choice | null> {
    const response = await apiRequest<Choice>('/choices', {
      method: 'POST',
      body: JSON.stringify({ text, nextNodeId }),
    });
    return response.data || null;
  },
};

/**
 * User API methods
 */
export const userAPI = {
  /**
   * Get all users
   */
  async getAllUsers(): Promise<User[]> {
    const response = await apiRequest<User[]>('/users');
    return response.data || [];
  },

  /**
   * Get a specific user
   */
  async getUser(userId: number): Promise<User | null> {
    const response = await apiRequest<User>(`/users/${userId}`);
    return response.data || null;
  },

  /**
   * Create a new user
   */
  async createUser(
    username: string,
    email: string,
    password: string
  ): Promise<User | null> {
    const response = await apiRequest<User>('/users', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
    return response.data || null;
  },

  /**
   * Get user's story progress
   */
  async getUserProgress(userId: number): Promise<unknown> {
    const response = await apiRequest(`/users/${userId}/progress`);
    return response.data || null;
  },

  /**
   * Save user's story progress
   */
  async saveUserProgress(
    userId: number,
    storyId: number,
    nodeId: number
  ): Promise<boolean> {
    const response = await apiRequest(`/users/${userId}/save`, {
      method: 'POST',
      body: JSON.stringify({ storyId, nodeId }),
    });
    return response.status === 'success';
  },
};
