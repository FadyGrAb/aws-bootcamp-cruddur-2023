import { request } from "urllib";

(async () => {
  try {
    const result = await request("http://localhost:5555/", { method: "GET" });
    console.log(result);
    if (result.status === 200) {
      process.exit(0);
    } else {
      process.exit(1);
    }
  } catch (error) {
    console.log(error);
    process.exit(1);
  }
})();
