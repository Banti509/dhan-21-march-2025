
import React from "react";
// import Button from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";


export default function DashboardContent() {
  return (
    <div className="mt-6 grid grid-cols-3 gap-6">
      <Card className="bg-gray-900 p-4 border border-yellow-500">
        <CardContent>
          <p className="text-lg font-bold">Create Order</p>
          {/* <p className="text-green-400 mt-2"></p> */}
        </CardContent>
      </Card>
      <Card className="bg-gray-900 p-4 border border-yellow-500">
        <CardContent className="flex flex-col gap-3">
          <p className="text-lg font-bold">Modify Order</p>
          {/* <Button className="bg-yellow-400 text-black">Deposit</Button> */}
        </CardContent>
      </Card>
      <Card className="bg-gray-900 p-4 border border-yellow-500">
        <CardContent>
          <p className="text-lg font-bold">Cancel Order</p>
          {/* <p className="text-gray-400 mt-2">⏳ Pending</p> */}
        </CardContent>
      </Card>
      <Card className="bg-gray-900 p-4 border border-yellow-500">
        <CardContent>
          <p className="text-lg font-bold">PNL Report & Order Sell</p>
          {/* <p className="text-gray-400 mt-2">⏳ Pending</p> */}
        </CardContent>
      </Card>
    </div>
  );
}

