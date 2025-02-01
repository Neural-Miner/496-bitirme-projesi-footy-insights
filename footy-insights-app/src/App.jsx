import './App.css';
import React, { useState, useRef } from 'react';
// import videoBg from './assets/background_video_2.mp4'
import videoBg from './assets/background_video.mp4'

import { FaPlay, FaPause } from "react-icons/fa"; // oynat-duraklat ikonlari

function App() {

  const videoRef = useRef(null); // video kontrolu
  const [isPlaying, setIsPlaying] = useState(true);

  const togglePlayPause = () => {
    if (videoRef.current.paused) {
      videoRef.current.play();
      setIsPlaying(true);
    } else {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  return (
    <div className="App">
      <div className="overlay"></div>
        <video src={videoBg} autoPlay loop muted />
          <div className="content">
            <UploadBox />
          </div>
      <button className="playPauseButton" onClick={togglePlayPause}>
        {isPlaying ? <FaPause /> : <FaPlay />}
      </button>
    </div>
  );
}

const UploadBox = () => {

  const [video, setVideo] = useState(null);

  const handleVideoUpload = (e) => {
    setVideo(e.target.files[0]);
    alert(`${e.target.files[0].name} yüklendi!`);
  };

  return (
    <>

    <div className="container">

      <div className="form-group">
          <label className="label" htmlFor="videoUpload">
            Maç videosunu yükleyiniz:
          </label>
          <input type="file" id="video" accept="video/*" className="input" onChange={handleVideoUpload}/>
      </div>

      <div>
        <label className='label' htmlFor='homeTeam'>
          Ev Sahibi Takım:
        </label>
        <input type='text' id='homeTeam' placeholder='Ev sahibi takımı giriniz' className='input'/>
      </div>

      <div>
        <label className='label' htmlFor='awayTeam'>
          Deplasman Takımı:
        </label>
        <input type='text' id='awayTeam' placeholder='Deplasman takımı giriniz' className='input'/>
      </div>

      <div className="form-group">
          <label className="label" htmlFor="season">
            Sezon:
          </label>
          <input type="text" id="season" placeholder="(örn. 2023-2024)" className="input"
          />
        </div>

        <div className="form-group">
          <label className="label" htmlFor="week">
            Hafta:
          </label>
          <input type="number" id="week" placeholder="(örn. 8)" min={1}
            className="input"
          />
        </div>

        

    </div>
    </>
  );
};

export default App;