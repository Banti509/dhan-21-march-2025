

import React from "react";
import Button from "../components/ui/button";
import { Search, Bell, Globe, Moon } from "lucide-react";
// import { Button } from "@/components/ui/button";

export default function Header() {
  return (
    <div className="flex justify-between items-center">
      <div className="flex items-center gap-2">
        {/* <User className="bg-gray-800 p-2 rounded-full" /> */}
        <h1 className="text-xl font-bold text-green-500">Dhan Trading Bot</h1>
        </div>
      <div className="flex gap-3 items-center">
        <Search />
        <Bell />
        <Globe />
        <Moon />
        <Button className="bg-green-500 text-black">Deposit</Button>
      </div>
    </div>
  );
}