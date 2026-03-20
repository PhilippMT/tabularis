import { invoke } from "@tauri-apps/api/core";
import { useCallback, useEffect, useState } from "react";

import type { RegistryPluginWithStatus } from "../types/plugins";

function isTauriRuntimeAvailable(): boolean {
  if (typeof window === "undefined") return false;
  const w = window as Window & {
    __TAURI_INTERNALS__?: {
      invoke?: unknown;
    };
  };
  return typeof w.__TAURI_INTERNALS__?.invoke === "function";
}

export function usePluginRegistry(): {
  plugins: RegistryPluginWithStatus[];
  loading: boolean;
  error: string | null;
  refresh: () => void;
} {
  const [plugins, setPlugins] = useState<RegistryPluginWithStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(() => {
    if (!isTauriRuntimeAvailable()) {
      setPlugins([]);
      setLoading(false);
      setError(
        "Plugin registry is only available in the Tauri desktop runtime. Start the app with `npm run tauri dev`."
      );
      return;
    }

    invoke<RegistryPluginWithStatus[]>("fetch_plugin_registry")
      .then((result) => {
        setPlugins(result);
        setError(null);
      })
      .catch((err: unknown) => {
        setError(String(err));
      })
      .finally(() => setLoading(false));
  }, []);

  const refresh = useCallback(() => {
    setLoading(true);
    setError(null);
    load();
  }, [load]);

  useEffect(() => {
    load();
  }, [load]);

  return { plugins, loading, error, refresh };
}
