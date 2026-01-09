// frontend/src/components/UnicornBackground.jsx
import React, { useEffect, useRef, useState } from "react";

export default function UnicornBackground() {
  const unicornRef = useRef(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const wrapper = unicornRef.current;
    if (!wrapper) return;

    // create or reuse projectDiv — attach to document.body to avoid clipping
    let projectDiv = document.querySelector("[data-us-project]");
    if (!projectDiv) {
      projectDiv = document.createElement("div");
      projectDiv.setAttribute("data-us-project", "p4VdxnnHjOL82ic0CzsJ");

      Object.assign(projectDiv.style, {
        position: "fixed",
        top: "0",
        left: "0",
        right: "0",
        bottom: "0",
        width: "auto",
        height: "auto",
        overflow: "hidden",
        margin: "0",
        padding: "0",
        zIndex: "-9999",        // ⬅️ ALWAYS behind everything
        pointerEvents: "none",
        boxSizing: "border-box",
        opacity: "0",
        transition: "opacity 600ms ease",
        background:
          "radial-gradient(circle at 20% 30%, #1a1a1f 0%, #0d0d0f 100%)"
      });

      document.body.appendChild(projectDiv);
    } else {
      Object.assign(projectDiv.style, {
        position: "fixed",
        top: "0",
        left: "0",
        right: "0",
        bottom: "0",
        zIndex: "-9999"   // ⬅️ ensure always behind
      });
    }

    if (window.UnicornStudio?.isInitialized) {
      projectDiv.style.opacity = "1";
      setTimeout(() => setIsLoaded(true), 350);
      return;
    }

    if (window.__UNICORN_LOADING__) {
      const poll = setInterval(() => {
        if (window.UnicornStudio?.isInitialized) {
          clearInterval(poll);
          projectDiv.style.opacity = "1";
          setTimeout(() => setIsLoaded(true), 350);
        }
      }, 150);
      return () => clearInterval(poll);
    }

    window.__UNICORN_LOADING__ = true;

    const script = document.createElement("script");
    script.src =
      "https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.34/dist/unicornStudio.umd.js";
    script.async = true;
    script.crossOrigin = "anonymous";

    const showBackground = () => {
      projectDiv.style.opacity = "1";

      requestAnimationFrame(() => {
        const canvas = projectDiv.querySelector("canvas");
        if (canvas) {
          canvas.style.width = "100%";
          canvas.style.height = "100%";
        }
      });

      setTimeout(() => {
        setIsLoaded(true);
        window.__UNICORN_LOADING__ = false;
      }, 520);
    };

    script.onload = () => {
      try {
        window.UnicornStudio.init?.();
        window.UnicornStudio.isInitialized = true;
      } catch {}
      showBackground();
    };

    script.onerror = showBackground;

    document.body.appendChild(script);

    const onResize = () => {
      const canvas = projectDiv.querySelector("canvas");
      if (canvas) {
        canvas.style.width = "100%";
        canvas.style.height = "100%";
      }
    };

    window.addEventListener("resize", onResize);
    window.addEventListener("orientationchange", onResize);

    return () => {
      window.removeEventListener("resize", onResize);
      window.removeEventListener("orientationchange", onResize);
    };
  }, []);

  return (
    <div
      ref={unicornRef}
      className="fixed inset-0 w-full h-full"
      style={{
        background: "radial-gradient(circle at 20% 30%, #1a1a1f 0%, #0d0d0f 100%)",
        overflow: "hidden",
        zIndex: -9999  // ⬅️ BACKGROUND LAYER ONLY
      }}
    >
      {/* Loader overlay */}
      <div
        className="absolute inset-0 flex flex-col items-center justify-center transition-all duration-500"
        style={{
          zIndex: -9998, // Loader ALSO behind UI
          background: "rgba(0,0,0,0.6)",
          opacity: isLoaded ? 0 : 1,
          pointerEvents: "none",
          transform: isLoaded ? "scale(1.02)" : "scale(1)",
          filter: isLoaded ? "blur(2px)" : "blur(0px)"
        }}
      >
        <div
          className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2"
          style={{ borderColor: "#a88fd8" }}
        />
        <p className="mt-4 text-gray-300 text-sm tracking-wide">
          Loading AdVision environment...
        </p>
      </div>
    </div>
  );
}
