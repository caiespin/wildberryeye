// components/EmblaCarousel.js
import React from "react";
import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";
import "./Carousel.css";

const EmblaCarousel = ({ images }) => {
  const [emblaRef] = useEmblaCarousel({ loop: true }, [
    Autoplay({ delay: 2000 }),
  ]);
  const allImages = images;

  return (
    <div className="embla" ref={emblaRef}>
      <div className="embla__container">
        {allImages.map((item, index) => (
          <div className="embla__slide" key={index}>
            <img src={item.src} alt={item.alt} className="embla_image" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default EmblaCarousel;
