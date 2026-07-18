import { describe, expect, it } from "vitest";
import { cn, formatDelta, formatNumber, formatPercent } from "./utils";

describe("cn", () => {
  it("merges class names", () => {
    expect(cn("a", "b")).toBe("a b");
  });

  it("resolves tailwind conflicts (last wins)", () => {
    expect(cn("p-2", "p-4")).toBe("p-4");
  });

  it("drops falsy values", () => {
    expect(cn("a", false, undefined, "b")).toBe("a b");
  });
});

describe("formatNumber", () => {
  it("adds thousands separators", () => {
    expect(formatNumber(1284)).toBe("1,284");
  });
});

describe("formatPercent", () => {
  it("formats a ratio as a percent", () => {
    expect(formatPercent(0.87)).toBe("87%");
  });

  it("supports fractional digits", () => {
    expect(formatPercent(0.875, 1)).toBe("87.5%");
  });
});

describe("formatDelta", () => {
  it("prefixes positive deltas with +", () => {
    expect(formatDelta(8.2)).toBe("+8.2%");
  });

  it("keeps the minus sign for negatives", () => {
    expect(formatDelta(-4.1)).toBe("-4.1%");
  });
});
