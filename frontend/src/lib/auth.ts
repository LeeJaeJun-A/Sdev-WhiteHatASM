// auth.ts
import fastapi from "$lib/fastapi";
import { goto } from "$app/navigation";
import { setRole, setId, getRole, getId } from "$lib/store";
import Swal from "sweetalert2";

interface UserData {
  status: string;
  user: {
    exp: Date;
    id: string;
    role: string;
  };
}

interface ErrorData {
  detail: string;
}

const refreshToken = async (): Promise<string | null> => {
  const storedRefreshToken = localStorage.getItem("refresh_token");
  if (!storedRefreshToken) {
    return null;
  }

  try {
    const newTokens = await new Promise<{
      access_token: string;
      token_type: string;
    }>((resolve, reject) => {
      fastapi(
        "POST",
        "/refresh",
        {},
        resolve,
        reject,
        storedRefreshToken
      );
    });

    const { access_token } = newTokens;
    localStorage.setItem("access_token", access_token);
    return access_token;
  } catch (error) {
    return null;
  }
};

export const verifyToken = async (): Promise<{
  user: UserData | null;
  error: ErrorData | null;
}> => {
  const storedToken = localStorage.getItem("access_token");

  if (storedToken) {
    try {
      const userData: UserData = await new Promise((resolve, reject) => {
        fastapi("GET", "/verify-token", {}, resolve, reject, storedToken);
      });

      return { user: userData, error: null };
    } catch (err) {
      if ((err as ErrorData).detail === "Token has expired") {
        const newAccessToken = await refreshToken();
        if (newAccessToken) {
          return verifyToken();
        } else {
          return { user: null, error: { detail: "Failed to refresh token" } };
        }
      }
      return { user: null, error: err as ErrorData };
    }
  } else {
    return { user: null, error: { detail: "No token found" } };
  }
};

export function logout() {
  localStorage.setItem("access_token", "");
  localStorage.setItem("refresh_token", "");
  setId(null);
  setRole(null);
  window.location.href = '/';
}

export async function initializeSession() {
  const result = await verifyToken();
  if (result.error !== null) {
    Swal.fire({
      icon: 'error',
      title: 'Unusual Approach',
      text: 'Return to home page',
    });
    logout();
  } else {
    if (
      typeof window !== 'undefined' &&
      (getRole() === null || getId() === null)
    ) {
      setRole(result.user?.user.role || null);
      setId(result.user?.user.id || null);
    }
  }
}
