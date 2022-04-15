import * as React from 'react';

const GreenTickLogo = ({ height = "16", width = "16", style = "" }) => 
    <svg 
        width={width}
        height={height}
        viewBox="0 0 16 16" 
        xmlns="http://www.w3.org/2000/svg" 
        className={style}
        focusable="false" role="img" aria-hidden="true">
            <path fill-rule="evenodd" d="M6.5 12a.502.502 0 01-.354-.146l-4-4a.502.502 0 01.708-.708L6.5 10.793l6.646-6.647a.502.502 0 01.708.708l-7 7A.502.502 0 016.5 12">
            </path>
    </svg>

export default GreenTickLogo;
