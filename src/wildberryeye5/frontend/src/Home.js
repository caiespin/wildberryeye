import React, { useEffect, useState } from "react";
import EmblaCarousel from "./components/EmblaCarousel";
import "./App.css";

const logos = [
  { src: "/images/1.jpg", alt: "bees1 Logo" },
  { src: "/images/2.jpg", alt: "bees2 Logo" },
  { src: "/images/3.jpg", alt: "bees3 Logo" },
  { src: "/images/4.jpg", alt: "bees4 Logo" },
  { src: "/images/5.jpg", alt: "bees5 Logo" },
];

const Home = () => {
  const [msg, setMsg] = useState("");
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(timer); // cleanup
  }, []);

  useEffect(() => {
    fetch("/api/hello")
      .then((res) => res.json())
      .then((data) => setMsg(data.message))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      {/* <h1>{msg}</h1> */}
      <div className="background-wrapper">
        <h1>Welcome to WildberryEye Platform!</h1>
      </div>
      <div className="liveview">
        <h1>Live Preview for HummingBirds!</h1>
        <p>Time: {time.toLocaleString()}</p>
        <EmblaCarousel images={logos} />
        <button className="download-button">Download</button>
      </div>
    </div>
  );
};

export default Home;
