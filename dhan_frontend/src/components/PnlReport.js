
// ####################################################################################################################################

// import React, { useEffect, useState, useCallback } from "react";
// import { io } from "socket.io-client";

// const socket = io("http://127.0.0.1:5000", {
//     transports: ["websocket"], 
//     reconnectionAttempts: 5,   
//     reconnectionDelay: 2000,    
// });

// const PnlReport = () => {
//     const [pnlData, setPnlData] = useState([]);
//     const [livePrices, setLivePrices] = useState({});  
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     const fetchInitialData = async () => {
//         try {
//             const response = await fetch("http://127.0.0.1:5000/api/pnl-report");
//             if (!response.ok) {
//                 throw new Error(`HTTP error! Status: ${response.status}`);
//             }
//             const data = await response.json();
//             console.log("✅ Initial API Data:", data);

//             if (data.status === "success") {
//                 setPnlData(data.orders || []);
//                 setLivePrices(data.live_prices || {});
//             } else {
//                 throw new Error("Invalid API response structure.");
//             }
//         } catch (err) {
//             console.error("Error fetching initial data:", err);
//             setError("Failed to fetch initial data.");
//         }
//         setLoading(false);
//     };

//     const handlePnLUpdate = useCallback((data) => {
//         console.log("🔄 WebSocket Received Update:", data);

//         if (data.status === "success" && data.live_prices) {
//             setLivePrices(prevLivePrices => ({
//                 ...prevLivePrices,
//                 ...data.live_prices,
//             }));
//         } else {
//             setError("Invalid WebSocket data.");
//         }
//     }, []);

//     useEffect(() => {
//         fetchInitialData();

//         socket.on("pnl_update", handlePnLUpdate);
//         socket.on("connect", () => console.log("✅ WebSocket connected!"));
//         socket.on("disconnect", () => console.log("❌ WebSocket disconnected!"));
//         socket.on("connect_error", (err) => {
//             console.error("WebSocket connection error:", err.message || err);
//             setError("WebSocket connection failed.");
//         });

//         return () => {
//             socket.off("pnl_update", handlePnLUpdate);
//         };
//     }, [handlePnLUpdate]);

//     const totalPnL = pnlData.reduce((sum, order) => {
//         const currentPrice = livePrices[order.security_id] || order.price;
//         return sum + (currentPrice - order.price) * order.quantity;
//     }, 0).toFixed(2);

//     const totalPnLPercentage = pnlData.reduce((sum, order) => {
//         const currentPrice = livePrices[order.security_id] || order.price;
//         return sum + (((currentPrice - order.price) / order.price) * 100);
//     }, 0).toFixed(2);

//     return (
//         <div className="p-6 bg-gray-900 min-h-screen flex flex-col items-center text-white">
//             <h2 className="text-2xl font-bold mb-4">📊 Live PnL Report</h2>
//             {loading ? (
//                 <p className="text-gray-300">Fetching data...</p>
//             ) : error ? (
//                 <p className="text-red-500 font-semibold">{error}</p>
//             ) : (
//                 <div className="w-full max-w-5xl bg-gray-800 shadow-md rounded-lg overflow-hidden">
//                     <div className="overflow-x-auto">
//                         <table className="w-full text-sm text-gray-300">
//                             <thead className="bg-blue-600 text-white uppercase text-xs">
//                                 <tr>
//                                     <th className="px-4 py-2">Order ID</th>
//                                     <th className="px-4 py-2">Security ID</th>
//                                     <th className="px-4 py-2">Type</th>
//                                     <th className="px-4 py-2">Quantity</th>
//                                     <th className="px-4 py-2">Entry Price</th>
//                                     <th className="px-4 py-2">Latest Price</th>
//                                     <th className="px-4 py-2">PnL</th>
//                                     <th className="px-4 py-2">PnL %</th>
//                                     <th className="px-4 py-2">Profit/Loss</th>
//                                 </tr>
//                             </thead>
//                             <tbody className="divide-y divide-gray-700">
//                                 {pnlData.length === 0 ? (
//                                     <tr>
//                                         <td colSpan="9" className="p-4 text-center text-gray-500">
//                                             No orders available.
//                                         </td>
//                                     </tr>
//                                 ) : (
//                                     pnlData.map((order) => {
//                                         const currentPrice = livePrices[order.security_id] || order.price;
//                                         const pnl = ((currentPrice - order.price) * order.quantity).toFixed(2);
//                                         const pnlPercentage = (((currentPrice - order.price) / order.price) * 100).toFixed(2);
//                                         const profitLoss = pnl >= 0 ? "Profit" : "Loss";
//                                         return (
//                                             <tr key={order.order_id} className="hover:bg-gray-700">
//                                                 <td className="px-4 py-2">{order.order_id || "N/A"}</td>
//                                                 <td className="px-4 py-2">{order.security_id || "N/A"}</td>
//                                                 <td className="px-4 py-2">{order.transaction_type || "N/A"}</td>
//                                                 <td className="px-4 py-2">{order.quantity || "N/A"}</td>
//                                                 <td className="px-4 py-2">{order.price || "N/A"}</td>
//                                                 <td className="px-4 py-2 text-yellow-400 font-semibold">{currentPrice}</td>
//                                                 <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{pnl}</td>
//                                                 <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{pnlPercentage}%</td>
//                                                 <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{profitLoss}</td>
//                                             </tr>
//                                         );
//                                     })
//                                 )}
//                             </tbody>
//                             <tfoot className="bg-gray-700 text-white font-bold">
//                                 <tr>
//                                     <td colSpan="6" className="px-6 py-2 text-left">Total   :-</td>
//                                     <td className={`px-4 py-2 ${totalPnL >= 0 ? "text-green-500" : "text-red-500"}`}>{totalPnL}</td>
//                                     <td className={`px-4 py-2 ${totalPnLPercentage >= 0 ? "text-green-500" : "text-red-500"}`}>{totalPnLPercentage}%</td>
//                                     <td className="px-4 py-2">—</td>
//                                 </tr>
//                             </tfoot>
//                         </table>
//                     </div>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default PnlReport;


// ##########################################################################################################################################





// import React, { useEffect, useState, useCallback } from "react";
// import { io } from "socket.io-client";

// const socket = io("http://127.0.0.1:5000", {
//     transports: ["websocket"],
//     reconnectionAttempts: 5,
//     reconnectionDelay: 2000,
//     forceNew: true,
//     path: "/socket.io",
// });

// const PnlReport = () => {
//     const [pnlData, setPnlData] = useState([]);
//     const [livePrices, setLivePrices] = useState({});
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     const fetchInitialData = async () => {
//         try {
//             const response = await fetch("http://127.0.0.1:5000/api/pnl-report");
//             if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

//             const data = await response.json();
//             console.log("✅ Initial API Data:", data);

//             if (data.status === "success") {
//                 setPnlData(data.orders.map(order => ({
//                     ...order,
//                     latest_price: data.live_prices[order.security_id] ?? order.price,
//                 })));
//                 setLivePrices(data.live_prices || {});
//             } else {
//                 throw new Error("Invalid API response structure.");
//             }
//         } catch (err) {
//             console.error("Error fetching initial data:", err);
//             setError("Failed to fetch initial data.");
//         }
//         setLoading(false);
//     };

//     const handlePnLUpdate = useCallback((data) => {
//         console.log("🔄 WebSocket Received Update:", data);
    
//         if (!data || data.status !== "success" || !data.pnl_report) {
//             console.error("❌ Invalid WebSocket data received:", data);
//             setError("Invalid WebSocket data.");
//             return;
//         }
    
//         // Extract updated prices from WebSocket data
//         const updatedPrices = data.pnl_report.reduce((acc, order) => {
//             acc[order.security_id] = order.current_price;
//             return acc;
//         }, {});
    
//         console.log("✅ Extracted Live Prices:", updatedPrices);
    
//         // Update livePrices state
//         setLivePrices(prev => {
//             const newPrices = { ...prev, ...updatedPrices };
//             console.log("✅ Updated Live Prices State:", newPrices);
//             return newPrices;
//         });
    
//         // Update pnlData state with latest prices
//         setPnlData(prev => {
//             const updatedData = prev.map(order => {
//                 const newPrice = updatedPrices[order.security_id] ?? order.latest_price ?? order.price;
//                 return { ...order, latest_price: newPrice };
//             });
//             console.log("✅ Updated PnL Data:", updatedData);
//             return updatedData; // Return a new array to ensure re-render
//         });
//     }, []);

//     useEffect(() => {
//         fetchInitialData();

//         console.log("✅ Setting up WebSocket listeners...");
//         socket.on("connect", () => {
//             console.log("✅ WebSocket Connected!", socket.id);
//         });
//         socket.on("disconnect", () => console.log("❌ WebSocket Disconnected!"));
//         socket.on("connect_error", (err) => console.error("❌ WebSocket connection error:", err));
//         socket.on("pnl_update", handlePnLUpdate);
//         socket.on("test_event", (data) => console.log("🔔 Test Event Received:", data));
//         socket.on("any", (event, data) => console.log("🔍 Any Event Received:", event, data));  // Catch all events

//         return () => {
//             console.log("🛑 Cleaning up WebSocket listeners...");
//             socket.off("connect");
//             socket.off("disconnect");
//             socket.off("connect_error");
//             socket.off("pnl_update", handlePnLUpdate);
//             socket.off("test_event");
//             socket.off("any");
//         };
//     }, [handlePnLUpdate]);

//     const totalPnL = pnlData.reduce((sum, order) => {
//         const currentPrice = order.latest_price ?? order.price; // Simplified fallback
//         const multiplier = order.transaction_type === "BUY" ? 1 : -1;
//         return sum + (currentPrice - order.price) * order.quantity * multiplier;
//     }, 0).toFixed(2);
    
//     const totalPnLPercentage = pnlData.reduce((sum, order) => {
//         const currentPrice = order.latest_price ?? order.price;
//         const multiplier = order.transaction_type === "BUY" ? 1 : -1;
//         return sum + (((currentPrice - order.price) / order.price) * 100) * multiplier;
//     }, 0).toFixed(2);

//     console.log("🔍 Rendering with pnlData:", pnlData);

//     return (
//         <div className="p-6 bg-gray-900 min-h-screen flex flex-col items-center text-white">
//             <h2 className="text-2xl font-bold mb-4">📊 Live PnL Report</h2>
//             {loading ? (
//                 <p className="text-gray-300">Fetching data...</p>
//             ) : error ? (
//                 <p className="text-red-500 font-semibold">{error}</p>
//             ) : (
//                 <div className="w-full max-w-5xl bg-gray-800 shadow-md rounded-lg overflow-hidden">
//                     <div className="overflow-x-auto">
//                         <table className="w-full text-sm text-gray-300">
//                             <thead className="bg-blue-600 text-white uppercase text-xs">
//                                 <tr>
//                                     <th className="px-4 py-2">Order ID</th>
//                                     <th className="px-4 py-2">Security ID</th>
//                                     <th className="px-4 py-2">Type</th>
//                                     <th className="px-4 py-2">Quantity</th>
//                                     <th className="px-4 py-2">Entry Price</th>
//                                     <th className="px-4 py-2">Latest Price</th>
//                                     <th className="px-4 py-2">PnL</th>
//                                     <th className="px-4 py-2">PnL %</th>
//                                     <th className="px-4 py-2">Profit/Loss</th>
//                                 </tr>
//                             </thead>
//                             <tbody className="divide-y divide-gray-700">
//                                 {pnlData.length === 0 ? (
//                                     <tr>
//                                         <td colSpan="9" className="p-4 text-center text-gray-500">
//                                             No orders available.
//                                         </td>
//                                     </tr>
//                                 ) : (
//                                     pnlData.map((order) => {
//                                         const currentPrice = order.latest_price ?? order.price;
//                                         const multiplier = order.transaction_type === "BUY" ? 1 : -1;
//                                         const pnl = ((currentPrice - order.price) * order.quantity * multiplier).toFixed(2);
//                                         const pnlPercentage = (((currentPrice - order.price) / order.price) * 100 * multiplier).toFixed(2);
//                                         const profitLoss = pnl >= 0 ? "Profit" : "Loss";
//                                         return (
//                                             <tr key={order.order_id} className="hover:bg-gray-700">
//                                                 <td className="px-4 py-2">{order.order_id ?? "N/A"}</td>
//                                                 <td className="px-4 py-2">{order.security_id ?? "N/A"}</td>
//                                                 <td className="px-4 py-2">{order.transaction_type ?? "N/A"}</td>
//                                                 <td className="px-4 py-2">{order.quantity ?? "N/A"}</td>
//                                                 <td className="px-4 py-2">{order.price ?? "N/A"}</td>
//                                                 <td className="px-4 py-2 text-yellow-400 font-semibold">{currentPrice}</td>
//                                                 <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{pnl}</td>
//                                                 <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{pnlPercentage}%</td>
//                                                 <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{profitLoss}</td>
//                                             </tr>
//                                         );
//                                     })
//                                 )}
//                             </tbody>
//                             <tfoot className="bg-gray-700 text-white font-bold">
//                                 <tr>
//                                     <td colSpan="6" className="px-6 py-2 text-left">Total:</td>
//                                     <td className={`px-4 py-2 ${totalPnL >= 0 ? "text-green-500" : "text-red-500"}`}>{totalPnL}</td>
//                                     <td className={`px-4 py-2 ${totalPnLPercentage >= 0 ? "text-green-500" : "text-red-500"}`}>{totalPnLPercentage}%</td>
//                                     <td className="px-4 py-2">—</td>
//                                 </tr>
//                             </tfoot>
//                         </table>
//                     </div>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default PnlReport;




// import React, { useEffect, useState, useCallback } from "react";
// import { io } from "socket.io-client";

// const socket = io("http://127.0.0.1:5000", {
//     transports: ["websocket"],
//     reconnectionAttempts: 5,
//     reconnectionDelay: 2000,
// });

// const PnlReport = () => {
//     const [pnlData, setPnlData] = useState([]);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     const fetchInitialData = async () => {
//         try {
//             const response = await fetch("http://127.0.0.1:5000/api/pnl-report");
//             if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
//             const data = await response.json();
//             console.log("✅ Initial API Data:", data);

//             if (data.status === "success") {
//                 setPnlData(data.orders.map(order => ({
//                     ...order,
//                     current_price: data.live_prices[order.security_id] ?? order.price,
//                 })));
//             } else {
//                 throw new Error("Invalid API response structure.");
//             }
//         } catch (err) {
//             console.error("Error fetching initial data:", err);
//             setError("Failed to fetch initial data.");
//         } finally {
//             setLoading(false);
//         }
//     };

//     const handlePnLUpdate = useCallback((data) => {
//         console.log("🔄 WebSocket Update Received:", data);

//         if (data.status !== "success" || !data.pnl_report) {
//             console.error("❌ Invalid WebSocket data:", data);
//             setError("Invalid WebSocket data.");
//             return;
//         }

//         setPnlData(prev => {
//             const updatedData = data.pnl_report.map(report => ({
//                 order_id: report.order_id,
//                 security_id: report.security_id,
//                 transaction_type: report.transaction_type,
//                 quantity: report.quantity,
//                 price: report.entry_price, // Keep original price as "price"
//                 current_price: report.current_price, // Use current_price directly
//             }));
//             console.log("✅ Updated pnlData:", updatedData);
//             return updatedData; // Replace entire array for simplicity
//         });
//     }, []);

//     useEffect(() => {
//         fetchInitialData();

//         socket.on("connect", () => console.log("✅ WebSocket Connected:", socket.id));
//         socket.on("disconnect", () => console.log("❌ WebSocket Disconnected"));
//         socket.on("connect_error", (err) => console.error("❌ WebSocket Error:", err));
//         socket.on("pnl_update", handlePnLUpdate);

//         return () => {
//             socket.off("connect");
//             socket.off("disconnect");
//             socket.off("connect_error");
//             socket.off("pnl_update", handlePnLUpdate);
//         };
//     }, [handlePnLUpdate]);

//     const totalPnL = pnlData.reduce((sum, order) => {
//         const multiplier = order.transaction_type === "BUY" ? 1 : -1;
//         return sum + (order.current_price - order.price) * order.quantity * multiplier;
//     }, 0).toFixed(2);

//     const totalPnLPercentage = pnlData.reduce((sum, order) => {
//         const multiplier = order.transaction_type === "BUY" ? 1 : -1;
//         return sum + (((order.current_price - order.price) / order.price) * 100) * multiplier;
//     }, 0).toFixed(2);

//     return (
//         <div className="p-6 bg-gray-900 min-h-screen flex flex-col items-center text-white">
//             <h2 className="text-2xl font-bold mb-4">📊 Live PnL Report</h2>
//             {loading ? (
//                 <p className="text-gray-300">Fetching data...</p>
//             ) : error ? (
//                 <p className="text-red-500 font-semibold">{error}</p>
//             ) : (
//                 <div className="w-full max-w-5xl bg-gray-800 shadow-md rounded-lg overflow-hidden">
//                     <div className="overflow-x-auto">
//                         <table className="w-full text-sm text-gray-300">
//                             <thead className="bg-blue-600 text-white uppercase text-xs">
//                                 <tr>
//                                     <th className="px-4 py-2">Order ID</th>
//                                     <th className="px-4 py-2">Security ID</th>
//                                     <th className="px-4 py-2">Type</th>
//                                     <th className="px-4 py-2">Quantity</th>
//                                     <th className="px-4 py-2">Entry Price</th>
//                                     <th className="px-4 py-2">Live Price</th>
//                                     <th className="px-4 py-2">PnL</th>
//                                     <th className="px-4 py-2">PnL %</th>
//                                     <th className="px-4 py-2">Profit/Loss</th>
//                                 </tr>
//                             </thead>
//                             <tbody className="divide-y divide-gray-700">
//                                 {pnlData.length === 0 ? (
//                                     <tr>
//                                         <td colSpan="9" className="p-4 text-center text-gray-500">
//                                             No orders available.
//                                         </td>
//                                     </tr>
//                                 ) : (
//                                     pnlData.map((order) => {
//                                         const multiplier = order.transaction_type === "BUY" ? 1 : -1;
//                                         const pnl = ((order.current_price - order.price) * order.quantity * multiplier).toFixed(2);
//                                         const pnlPercentage = (((order.current_price - order.price) / order.price) * 100 * multiplier).toFixed(2);
//                                         const profitLoss = pnl >= 0 ? "Profit" : "Loss";
//                                         return (
//                                             <tr key={order.order_id} className="hover:bg-gray-700">
//                                                 <td className="px-4 py-2">{order.order_id}</td>
//                                                 <td className="px-4 py-2">{order.security_id}</td>
//                                                 <td className="px-4 py-2">{order.transaction_type}</td>
//                                                 <td className="px-4 py-2">{order.quantity}</td>
//                                                 <td className="px-4 py-2">{order.price}</td>
//                                                 <td className="px-4 py-2 text-yellow-400 font-semibold">{order.current_price}</td>
//                                                 <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{pnl}</td>
//                                                 <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{pnlPercentage}%</td>
//                                                 <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{profitLoss}</td>
//                                             </tr>
//                                         );
//                                     })
//                                 )}
//                             </tbody>
//                             <tfoot className="bg-gray-700 text-white font-bold">
//                                 <tr>
//                                     <td colSpan="6" className="px-6 py-2 text-left">Total:</td>
//                                     <td className={`px-4 py-2 ${totalPnL >= 0 ? "text-green-500" : "text-red-500"}`}>{totalPnL}</td>
//                                     <td className={`px-4 py-2 ${totalPnLPercentage >= 0 ? "text-green-500" : "text-red-500"}`}>{totalPnLPercentage}%</td>
//                                     <td className="px-4 py-2">—</td>
//                                 </tr>
//                             </tfoot>
//                         </table>
//                     </div>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default PnlReport;







import React, { useEffect, useState, useCallback } from "react";
import { io } from "socket.io-client";

// Initialize SocketIO connection
const socket = io("http://127.0.0.1:5000", {
    transports: ["websocket"],
    reconnectionAttempts: 5,
    reconnectionDelay: 2000,
});

const PnlReport = () => {
    const [pnlData, setPnlData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchInitialData = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/api/pnl-report");
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const data = await response.json();
            console.log("✅ Initial API Data:", data);

            if (data.status === "success") {
                setPnlData(data.orders.map(order => ({
                    ...order,
                    current_price: data.live_prices[order.security_id] ?? order.price,
                })));
            } else {
                throw new Error("Invalid API response structure.");
            }
        } catch (err) {
            console.error("Error fetching initial data:", err);
            setError("Failed to fetch initial data.");
        } finally {
            setLoading(false);
        }
    };

    const handlePnLUpdate = useCallback((data) => {
        console.log("🔄 WebSocket Update Received:", data);
    
        if (data.status !== "success" || !data.pnl_report) {
            console.error("❌ Invalid WebSocket data:", data);
            setError("Invalid WebSocket data.");
            return;
        }
    
        // Update only the current_price field while keeping other order details intact
        setPnlData((prevPnlData) => 
            prevPnlData.map(order => {
                const updatedOrder = data.pnl_report.find(item => item.order_id === order.order_id);
                return updatedOrder
                    ? { ...order, current_price: updatedOrder.current_price } // Update price only
                    : order;
            })
        );
    }, []);
    
    
    useEffect(() => {
        fetchInitialData(); // Fetch initial data on mount
    
        socket.on("connect", () => console.log("✅ WebSocket Connected:", socket.id));
        socket.on("disconnect", () => console.log("❌ WebSocket Disconnected"));
        socket.on("connect_error", (err) => console.error("❌ WebSocket Error:", err));
        
        // Listen for WebSocket price updates
        socket.on("pnl_update", handlePnLUpdate);
    
        return () => {
            socket.off("connect");
            socket.off("disconnect");
            socket.off("connect_error");
            socket.off("pnl_update", handlePnLUpdate);
        };
    }, [handlePnLUpdate]); // Ensures latest function reference
    

    // Debug log when pnlData changes
    useEffect(() => {
        console.log("📊 pnlData state updated:", pnlData);
    }, [pnlData]);

    const totalPnL = pnlData.reduce((sum, order) => {
        const multiplier = order.transaction_type === "BUY" ? 1 : -1;
        return sum + (order.current_price - order.price) * order.quantity * multiplier;
    }, 0).toFixed(2);

    const totalPnLPercentage = pnlData.reduce((sum, order) => {
        const multiplier = order.transaction_type === "BUY" ? 1 : -1;
        return sum + (((order.current_price - order.price) / order.price) * 100) * multiplier;
    }, 0).toFixed(2);

    return (
        <div className="p-6 bg-gray-900 min-h-screen flex flex-col items-center text-white">
            <h2 className="text-2xl font-bold mb-4">📊 Live PnL Report</h2>
            {loading ? (
                <p className="text-gray-300">Fetching data...</p>
            ) : error ? (
                <p className="text-red-500 font-semibold">{error}</p>
            ) : (
                <div className="w-full max-w-5xl bg-gray-800 shadow-md rounded-lg overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-gray-300">
                            <thead className="bg-blue-600 text-white uppercase text-xs">
                                <tr>
                                    <th className="px-4 py-2">Order ID</th>
                                    <th className="px-4 py-2">Security ID</th>
                                    <th className="px-4 py-2">Type</th>
                                    <th className="px-4 py-2">Quantity</th>
                                    <th className="px-4 py-2">Entry Price</th>
                                    <th className="px-4 py-2">Live Price</th>
                                    <th className="px-4 py-2">PnL</th>
                                    <th className="px-4 py-2">PnL %</th>
                                    <th className="px-4 py-2">Profit/Loss</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-700">
                                {pnlData.length === 0 ? (
                                    <tr>
                                        <td colSpan="9" className="p-4 text-center text-gray-500">
                                        No orders available.
                                    </td>
                                    </tr>
                                ) : (
                                    pnlData.map((order) => {
                                        const multiplier = order.transaction_type === "BUY" ? 1 : -1;
                                        const pnl = ((order.current_price - order.price) * order.quantity * multiplier).toFixed(2);
                                        const pnlPercentage = (((order.current_price - order.price) / order.price) * 100 * multiplier).toFixed(2);
                                        const profitLoss = pnl >= 0 ? "Profit" : "Loss";
                                        return (
                                            <tr key={`${order.order_id}-${order.security_id}`} className="hover:bg-gray-700">
                                                <td className="px-4 py-2">{order.order_id}</td>
                                                <td className="px-4 py-2">{order.security_id}</td>
                                                <td className="px-4 py-2">{order.transaction_type}</td>
                                                <td className="px-4 py-2">{order.quantity}</td>
                                                <td className="px-4 py-2">{order.price}</td>
                                                <td className="px-4 py-2 text-yellow-400 font-semibold">{order.current_price}</td>
                                                <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{pnl}</td>
                                                <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{pnlPercentage}%</td>
                                                <td className={`px-4 py-2 ${pnl >= 0 ? "text-green-500" : "text-red-500"}`}>{profitLoss}</td>
                                            </tr>
                                        );
                                    })
                                )}
                            </tbody>
                            <tfoot className="bg-gray-700 text-white font-bold">
                                <tr>
                                    <td colSpan="6" className="px-6 py-2 text-left">Total:</td>
                                    <td className={`px-4 py-2 ${totalPnL >= 0 ? "text-green-500" : "text-red-500"}`}>{totalPnL}</td>
                                    <td className={`px-4 py-2 ${totalPnLPercentage >= 0 ? "text-green-500" : "text-red-500"}`}>{totalPnLPercentage}%</td>
                                    <td className="px-4 py-2">—</td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PnlReport;



