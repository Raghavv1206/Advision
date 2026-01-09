import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="relative h-screen w-screen overflow-hidden text-white flex flex-col">

      {/* NAVBAR */}
      <header
        className="absolute top-0 left-0 right-0 z-20 flex justify-between items-center px-9 py-3
          bg-transparent hover:bg-black/50 backdrop-blur-[3px] border-b border-white/10 
          transition-all duration-500 ease-in-out"
      >
        <div
          className="flex items-center space-x-2 cursor-pointer"
          onClick={() => navigate("/")}
        >
          <img
            src="/advisionlogo.png"
            alt="AdVision Logo"
            className="h-9 w-auto drop-shadow-[0_2px_6px_rgba(255,255,255,0.2)] transition-all duration-300 hover:scale-105"
          />
        </div>

        <nav className="flex items-center space-x-6">
          <Link
            to="/login"
            className="text-sm text-white/90 hover:text-[#BDA8C8] transition-all duration-300 relative 
              after:absolute after:bottom-0 after:left-0 after:h-[1px] after:w-0 after:bg-[#BDA8C8] 
              hover:after:w-full after:transition-all after:duration-300"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="text-sm font-semibold px-4 py-1.5 rounded-full text-[#ffffff] bg-gradient-to-r from-[#3a3440] to-[#a88fd8] 
              shadow-[0_0_15px_rgba(189,168,200,0.4)] hover:from-[#D6BCEB] hover:to-[#C8A9D0] 
              hover:scale-105 transition-all duration-300"
          >
            Get Started
          </Link>
        </nav>
      </header>

      {/* CTA BUTTON */}
      <div className="absolute bottom-7 left-0 right-0 flex justify-center z-10">
        <button
          onClick={() => navigate("/login")}
          className="px-12 py-4 text-xl font-semibold text-[#ffffff] bg-gradient-to-r from-[#3a3440] to-[#a88fd8] 
            rounded-full border border-[#BDA8C8]/30 backdrop-blur-md 
            shadow-[inset_0_0_15px_rgba(189,168,200,0.3),0_0_20px_rgba(189,168,200,0.2)]
            hover:shadow-[inset_0_0_20px_rgba(189,168,200,0.5),0_0_25px_rgba(189,168,200,0.4)]
            hover:scale-105 hover:brightness-110 transition-all duration-500"
        >
          Explore AdVision
        </button>
      </div>
    </div>
  );
}
