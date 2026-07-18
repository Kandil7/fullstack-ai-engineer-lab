import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { KpiCard } from "./KpiCard";

describe("KpiCard", () => {
  it("renders label, value, and positive delta", () => {
    render(<KpiCard kpi={{ label: "Active Users", value: "1,284", delta: 8.2 }} />);
    expect(screen.getByText("Active Users")).toBeInTheDocument();
    expect(screen.getByText("1,284")).toBeInTheDocument();
    expect(screen.getByText("+8.2%")).toBeInTheDocument();
  });

  it("renders negative delta with a minus sign", () => {
    render(<KpiCard kpi={{ label: "Cost / Query", value: "$0.006", delta: -4.1 }} />);
    expect(screen.getByText("-4.1%")).toBeInTheDocument();
  });
});
