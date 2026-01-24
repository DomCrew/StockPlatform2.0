import { useState } from "react";

export default function TickerSearch({ onSubmit }) {
  const [value, setValue] = useState("");

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      submit();
    }
  }

  function submit() {
    if (!value.trim()) return;
    onSubmit(value.toLowerCase());
  }

  return (
    <input
      type="text"
      placeholder="Enter ticker (e.g. AMZN)"
      value={value}
      onChange={e => setValue(e.target.value)}
      onKeyDown={handleKeyDown}
    />
  );
}