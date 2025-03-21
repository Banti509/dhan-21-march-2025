
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header"; 
import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import PlaceOrder from "./components/PlaceOrder";
import PnLReport from "./components/PnlReport";
// import ModifyOrder from "./components/ModifyOrder";
// import CancelOrder from "./components/OrderCancel";
// import OrderHistory from "./components/OrderHistory";
// import Dummypnlreport from "./components/DummyPnLReport";
import LoginPage from "./components/LoginPage";


const App = () => {
  const [selectedOrder, setSelectedOrder] = useState(null);

  return (
    <Router>
      <div className="bg-gray-900 text-white min-h-screen p-5">
        <Header />
        <div className="flex mt-5">
          <Sidebar setSelectedOrder={setSelectedOrder} />
          <div className="flex-1 p-5">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/place-order" element={<PlaceOrder />} />
              <Route path="/pnl-report" element={<PnLReport />} />
              <Route path="/LoginPage" element={<LoginPage />} />
              {/* <Route path="/modify-order" element={<ModifyOrder />} />
              <Route path="/cancel-order" element={<CancelOrder />} />
              <Route path="/binance_order" element={<OrderHistory />} />
              <Route path="/dummy_pnl_report" element={<Dummypnlreport />} /> */}
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
};

export default App;





// import React, { useState } from "react";
// import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// import Header from "./components/Header"; 
// import Sidebar from "./components/Sidebar";
// import Dashboard from "./components/Dashboard";
// import PlaceOrder from "./components/PlaceOrder";
// import PnLReport from "./components/PnlReport";
// // import ModifyOrder from "./components/ModifyOrder";
// // import CancelOrder from "./components/OrderCancel";
// // import OrderHistory from "./components/OrderHistory";
// // import Dummypnlreport from "./components/DummyPnLReport";
// import LoginPage from "./components/LoginPage";

// const App = () => {
//   const [isLoggedIn, setIsLoggedIn] = useState(false);
//   const [selectedOrder, setSelectedOrder] = useState(null);

//   const handleLogin = () => {
//     setIsLoggedIn(true);
//   };

//   return (
//     <Router>
//       <div className="bg-gray-900 text-white min-h-screen p-5">
//         {isLoggedIn ? (
//           <>
//             <Header />
//             <div className="flex mt-5">
//               <Sidebar setSelectedOrder={setSelectedOrder} />
//               <div className="flex-1 p-5">
//                 <Routes>
//                   <Route path="/" element={<Dashboard />} />
//                   <Route path="/place-order" element={<PlaceOrder />} />
//                   <Route path="/pnl-report" element={<PnLReport />} />
//                   {/* <Route path="/modify-order" element={<ModifyOrder />} />
//                   <Route path="/cancel-order" element={<CancelOrder />} />
//                   <Route path="/binance_order" element={<OrderHistory />} />
//                   <Route path="/dummy_pnl_report" element={<Dummypnlreport />} /> */}
//                 </Routes>
//               </div>
//             </div>
//           </>
//         ) : (
//           <Routes>
//             <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
//             <Route path="*" element={<Navigate to="/login" />} />
//           </Routes>
//         )}
//       </div>
//     </Router>
//   );
// };

// export default App;


