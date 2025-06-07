import React, { useEffect, useState } from "react";

const Home = () => {
  const [msg, setMsg] = useState("");

  useEffect(() => {
    fetch("/api/hello")
      .then((res) => res.json())
      .then((data) => setMsg(data.message))
      .catch((err) => console.error(err));
  }, []);
  return (
    <div>
      <h1>{msg}</h1>
      <h1>Welcome to the Home Page</h1>
    </div>
  );
};

export default Home;
