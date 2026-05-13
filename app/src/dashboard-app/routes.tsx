import { createBrowserRouter } from "react-router-dom";
import { RootLayout } from "./components/RootLayout";
import { LoginPage } from "./pages/LoginPage";
import { StudentDashboard } from "./pages/StudentDashboard";
import { AdminDashboard } from "./pages/AdminDashboard";
import { MaterialSearch } from "./pages/MaterialSearch";
import { LoanHistory } from "./pages/LoanHistory";
import { LoanConfirmation } from "./pages/LoanConfirmation";
import LandingPage from "../components/LandingPage";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: RootLayout,
    children: [
      { index: true, Component: LandingPage },
      { path: "login", Component: LoginPage },
      { path: "alumno", Component: StudentDashboard },
      { path: "admin", Component: AdminDashboard },
      { path: "buscar", Component: MaterialSearch },
      { path: "historial", Component: LoanHistory },
      { path: "prestamo/:id", Component: LoanConfirmation },
    ],
  },
]);
