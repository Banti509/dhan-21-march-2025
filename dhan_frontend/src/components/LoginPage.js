
// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { FaEye, FaEyeSlash } from "react-icons/fa";

// const Login = () => {
//   const navigate = useNavigate();
//   const [name, setName] = useState("");
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState(null);
//   const [message, setMessage] = useState("");
//   const [showPassword, setShowPassword] = useState(false);

//   const handleLogin = async (e) => {
//     e.preventDefault();
//     setError(null);
//     setMessage("");

//     const response = await fetch("http://localhost:5000/api/auth", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ action: "login", email, password }),
//     });

//     const data = await response.json();
//     if (response.ok) {
//       setMessage(data.message);
//       navigate("/place-order"); // Redirect to dashboard after successful login
//     } else {
//       setError(data.error);
//     }
//   };

//   const handleSignUp = async (e) => {
//     e.preventDefault();
//     setError(null);
//     setMessage("");

//     const response = await fetch("http://localhost:5000/api/auth", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ action: "signup", name, email, password }),
//     });

//     const data = await response.json();
//     if (response.ok) {
//       setMessage(data.message);
//     } else {
//       setError(data.error);
//     }
//   };

//   const handleGoogleLogin = async () => {
//     const response = await fetch("http://localhost:5000/api/auth", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ action: "google_login", email }),
//     });

//     const data = await response.json();
//     if (response.ok) {
//       setMessage(data.message);
//       navigate("/dashboard"); // Redirect to dashboard after successful Google login
//     } else {
//       setError(data.error);
//     }
//   };

//   return (
//     <div className="flex screen bg-black-800 justify-center items-center">
//       {/* Login Form Container */}
//       <div className="bg-white p-10 shadow-lg rounded-lg w-full max-w-md">
//         <h1 className="text-3xl font-bold mb-4">Log in</h1>
//         <p className="text-gray-600 mb-6">Welcome !!! Please enter your details.</p>

//         {error && <p className="text-red-500">{error}</p>}
//         {message && <p className="text-green-500">{message}</p>}

//         <form onSubmit={handleLogin} className="w-full">
//           <label className="block mb-2 text-gray-700">Email</label>
//           <input
//             type="email"
//             placeholder="Enter your email"
//             className="w-full p-3 mb-4 border rounded-lg text-black placeholder-gray-500"
//             value={email}
//             onChange={(e) => setEmail(e.target.value)}
//             required
//           />

//           <label className="block mb-2 text-gray-700">Password</label>
//           <div className="relative w-full">
//             <input
//               type={showPassword ? "text" : "password"}
//               placeholder="Enter your password"
//               className="w-full p-3 mb-4 border rounded-lg text-black placeholder-gray-500 pr-10"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               required
//             />
//             {/* Eye Icon for Toggle Password Visibility */}
//             <span
//               className="absolute top-4 right-4 cursor-pointer text-gray-600"
//               onClick={() => setShowPassword(!showPassword)}
//             >
//               {showPassword ? <FaEye size={20} /> : <FaEyeSlash size={20} />}
//             </span>
//           </div>
//           <button type="submit" className="w-full p-3 bg-gradient-to-r from-orange-400 to-pink-400 text-white rounded-lg font-semibold">
//             Log in
//           </button>
//         </form>

//         <button onClick={handleGoogleLogin} className="w-full p-3 mt-3 border flex items-center justify-center rounded-lg text-gray-700">
//           <img src="https://www.svgrepo.com/show/355037/google.svg" alt="Google" className="w-5 h-5 mr-2" />
//           Log in with Google
//         </button>

//         <p className="mt-4 text-gray-600">
//           Don't have an account? <a href="#" className="text-blue-500" onClick={handleSignUp}>Sign up</a>
//         </p>

//         <button
//           onClick={() => navigate("/")}
//           className="w-full p-2 mt-3 bg-gray-500 text-white rounded hover:bg-gray-600"
//         >
//           Back to Dashboard
//         </button>
//       </div>
//     </div>
//   );
// };

// export default Login;







import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const Login = () => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [message, setMessage] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isSignUp, setIsSignUp] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);
    setMessage("");

    const response = await fetch("http://localhost:5000/api/auth", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "login", email, password }),
    });

    const data = await response.json();
    if (response.ok) {
      setMessage(data.message);
      navigate("/place-order"); // Redirect to dashboard after successful login
    } else {
      setError(data.error);
    }
  };

  const handleSignUp = async (e) => {
    e.preventDefault();
    setError(null);
    setMessage("");

    const response = await fetch("http://localhost:5000/api/auth", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "signup", name, email, password }),
    });

    const data = await response.json();
    if (response.ok) {
      setMessage(data.message);
      setIsSignUp(false); // Switch back to login form after successful signup
    } else {
      setError(data.error);
    }
  };

  const handleGoogleLogin = async () => {
    const response = await fetch("http://localhost:5000/api/auth", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "google_login", email }),
    });

    const data = await response.json();
    if (response.ok) {
      setMessage(data.message);
      navigate("/"); // Redirect to dashboard after successful Google login
    } else {
      setError(data.error);
    }
  };

  return (
    <div className="flex screen bg-black-800 justify-center items-center">
      {/* Login Form Container */}
      <div className="bg-white p-10 shadow-lg rounded-lg w-full max-w-md">
        <h1 className="text-3xl font-bold mb-4">{isSignUp ? "Sign Up" : "Log in"}</h1>
        <p className="text-gray-600 mb-6">Welcome !!! Please enter your details.</p>

        {error && <p className="text-red-500">{error}</p>}
        {message && <p className="text-green-500">{message}</p>}

        {isSignUp ? (
          // Sign Up Form
          <form onSubmit={handleSignUp} className="w-full">
            <label className="block mb-2 text-gray-700">Name</label>
            <input
              type="text"
              placeholder="Enter your name"
              className="w-full p-3 mb-4 border rounded-lg text-black placeholder-gray-500"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />

            <label className="block mb-2 text-gray-700">Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              className="w-full p-3 mb-4 border rounded-lg text-black placeholder-gray-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <label className="block mb-2 text-gray-700">Password</label>
            <div className="relative w-full">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                className="w-full p-3 mb-4 border rounded-lg text-black placeholder-gray-500 pr-10"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              {/* Eye Icon for Toggle Password Visibility */}
              <span
                className="absolute top-4 right-4 cursor-pointer text-gray-600"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEye size={20} /> : <FaEyeSlash size={20} />}
              </span>
            </div>
            <button type="submit" className="w-full p-3 bg-gradient-to-r from-orange-400 to-pink-400 text-white rounded-lg font-semibold">
              Sign Up
            </button>
          </form>
        ) : (
          // Login Form
          <form onSubmit={handleLogin} className="w-full">
            <label className="block mb-2 text-gray-700">Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              className="w-full p-3 mb-4 border rounded-lg text-black placeholder-gray-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <label className="block mb-2 text-gray-700">Password</label>
            <div className="relative w-full">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                className="w-full p-3 mb-4 border rounded-lg text-black placeholder-gray-500 pr-10"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              {/* Eye Icon for Toggle Password Visibility */}
              <span
                className="absolute top-4 right-4 cursor-pointer text-gray-600"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEye size={20} /> : <FaEyeSlash size={20} />}
              </span>
            </div>
            <button type="submit" className="w-full p-3 bg-gradient-to-r from-orange-400 to-pink-400 text-white rounded-lg font-semibold">
              Log in
            </button>
          </form>
        )}

        <button onClick={handleGoogleLogin} className="w-full p-3 mt-3 border flex items-center justify-center rounded-lg text-gray-700">
          <img src="https://www.svgrepo.com/show/355037/google.svg" alt="Google" className="w-5 h-5 mr-2" />
          Log in with Google
        </button>

        <p className="mt-4 text-gray-600">
          {isSignUp ? "Already have an account? " : "Don't have an account? "}
          <a href="#" className="text-blue-500" onClick={() => setIsSignUp(!isSignUp)}>
            {isSignUp ? "Log in" : "Sign up"}
          </a>
        </p>

        <button
          onClick={() => navigate("/")}
          className="w-full p-2 mt-3 bg-gray-500 text-white rounded hover:bg-gray-600"
        >
          Back to Dashboard
        </button>
      </div>
    </div>
  );
};

export default Login;