import React from 'react';
import logoGenIA from "../assets/img/gen-ia-product-hub-logo-png.png";

const Logo = () => {
  return (
    <div className="w-full h-[110px] flex justify-between items-center px-4">
      <a href="/">
        <img src={logoGenIA} alt="Logo of GenIA ProductHub" className="w-[270px]" />
      </a>
      <div className="w-[50px] h-[50px] rounded-full overflow-hidden">
        <img src="https://www.gravatar.com/avatar/" alt="Avatar" className="w-full h-full object-cover" />
      </div>
    </div>
  );
};

export default Logo;
