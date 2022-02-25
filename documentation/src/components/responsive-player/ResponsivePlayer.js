import React from "react";
import ReactPlayer from "react-player";

function ResponsivePlayer({url, loop, playing}) {
  return (
    <div
      className="relative rounded-lg shadow-lg"
      style={{paddingTop: "56.25%"}}
    >
      {/* /* Player ratio: 100 / (1280 / 720) */}
      <ReactPlayer
        className="absolute top-0 left-0"
        url={url}
        loop={loop}
        playing={playing}
        width="100%"
        height="100%"
        controls={true}
      />
    </div>
  );
}

export default ResponsivePlayer;
