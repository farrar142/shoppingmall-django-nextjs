import { Box, colors, Slider } from "@mui/material";
import type { NextPage } from "next";
import Head from "next/head";
import Image from "next/image";
import { ChangeEvent, useState } from "react";
import PieRender from "../components/test/PieRender";
import { TokenType } from "../src/types/accounts/accountsTypes";
import styles from "../styles/Home.module.css";
const Home: NextPage = (props) => {
  const [current, setCurrent] = useState<number>(30);
  const max = 200;
  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    if (typeof newValue == "number") {
      setCurrent(newValue);
    }
  };
  return (
    <Box>
      <PieRender
        max={max}
        value={current}
        onChange={(e: any, nv: number) => setCurrent(nv)}
      >
        <div>PieRender</div>
      </PieRender>
      <Slider
        aria-label="Volume"
        max={max}
        value={current}
        onChange={handleSliderChange}
      />
    </Box>
  );
};
export default Home;
