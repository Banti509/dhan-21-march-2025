

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Home, ClipboardList, Settings, User, ChevronDown } from "lucide-react";

export default function Sidebar({ setSelectedOrder }) {
  const [openDropdown, setOpenDropdown] = useState(null);
  const [openSubmenu, setOpenSubmenu] = useState(null); // Separate state for submenu
  const navigate = useNavigate();

  // Function to toggle main dropdowns (Orders, User Data History)
  const toggleDropdown = (dropdown) => {
    setOpenDropdown(openDropdown === dropdown ? null : dropdown);
    setOpenSubmenu(null); // Close any open submenu when switching main dropdown
  };

  // Function to toggle submenus (Spot Order inside Orders)
  const toggleSubmenu = (submenu) => {
    setOpenSubmenu(openSubmenu === submenu ? null : submenu);
  };

  return (
    <div className="w-64 p-4 border-r border-gray-700 flex flex-col gap-4">
      <nav className="flex flex-col gap-2">
        <button className="flex items-center gap-2 p-2 rounded-lg bg-gray-800">
          <Home /> Dashboard
        </button>

        {/* Orders Dropdown */}
        <div>
          <button
            className="flex items-center justify-between w-full p-2 rounded-lg hover:bg-gray-800"
            onClick={() => toggleDropdown("orders")}
          >
            <span className="flex items-center gap-2"><ClipboardList /> Orders</span>
            <ChevronDown className={`transition-transform ${openDropdown === "orders" ? "rotate-180" : ""}`} />
          </button>

          {openDropdown === "orders" && (
            <div className="ml-6 mt-2 flex flex-col gap-2">
              <button
                className="p-2 rounded-lg hover:bg-gray-700"
                onClick={() => toggleSubmenu("spotOrders")}
              >
                Spot Order
              </button>

              {openSubmenu === "spotOrders" && (
                <div className="ml-6 mt-2 flex flex-col gap-2">
                  <button className="p-2 rounded-lg hover:bg-gray-500" onClick={() => navigate('/place-order')}>
                    Create Order
                  </button>
                  <button className="p-2 rounded-lg hover:bg-gray-500" onClick={() => navigate('/pnl-report')}>
                    PNL Report
                  </button>
                  <button className="p-2 rounded-lg hover:bg-gray-500" onClick={() => navigate('/modify-order')}>
                    Order Modify
                  </button>
                  <button className="p-2 rounded-lg hover:bg-gray-500" onClick={() => navigate('/cancel-order')}>
                    Order Cancel
                  </button>
                  <button className="p-2 rounded-lg hover:bg-gray-500" onClick={() => navigate('/dummy_pnl_report')}>
                    Dummy Order PNL
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* User Data History Dropdown */}
        <div>
          <button
            className="flex items-center justify-between w-full p-2 rounded-lg hover:bg-gray-800"
            onClick={() => toggleDropdown("userHistory")}
          >
            <span className="flex items-center gap-2"><User /> User Data History</span>
            <ChevronDown className={`transition-transform ${openDropdown === "userHistory" ? "rotate-180" : ""}`} />
          </button>

          {openDropdown === "userHistory" && (
            <div className="ml-6 mt-2 flex flex-col gap-2">
              <button
                className="p-2 rounded-lg hover:bg-gray-700"
                onClick={() => toggleSubmenu("userDetails")}
              >
                Show Data
              </button>

              {openSubmenu === "userDetails" && (
                <div className="ml-6 mt-2 flex flex-col gap-2">
                  <button className="p-2 rounded-lg hover:bg-gray-600" onClick={() => navigate('/binance_order')}>
                    Order Details
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* User Account Dropdown */}
        <div>
          <button
            className="flex items-center justify-between w-full p-2 rounded-lg hover:bg-gray-800"
            onClick={() => toggleDropdown("Account")}
          >
            <span className="flex items-center gap-2"><User /> Account</span>
            <ChevronDown className={`transition-transform ${openDropdown === "Account" ? "rotate-180" : ""}`} />
          </button>

          {openDropdown === "Account" && (
            <div className="ml-6 mt-2 flex flex-col gap-2">
              <button
                className="p-2 rounded-lg hover:bg-gray-700" onClick={() => navigate('/LoginPage')}>
                Create New Account
              </button>
            </div>
          )}
        </div>


        {/* <button className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-800">
          <User /> Account
        </button> */}
        <button className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-800">
          <Settings /> Settings
        </button>
      </nav>
    </div>
  );
}
