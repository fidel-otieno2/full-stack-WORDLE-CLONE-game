import React from 'react';
import "../styles/Tile.css";

function Tile({ value, status }) {
  return (
    <div className={`tile ${status || ""}`}>
      {value}
    </div>
  );
}

export default Tile;
