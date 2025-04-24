import React from "react";
import "./BackgroundVideo.css";

const BackgroundVideo = () => {
  return (
    <div className="background-container">
      <video autoPlay loop muted className="background-video">
        <source src="/background_video.mp4" type="video/mp4" />
        Tarayıcınız video etiketini desteklemiyor.
      </video>
    </div>
  );
};

export default BackgroundVideo;
