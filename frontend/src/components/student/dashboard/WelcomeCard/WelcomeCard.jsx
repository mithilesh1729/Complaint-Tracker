import useAuth from "../../../../hooks/useAuth";

import "./WelcomeCard.css";

function WelcomeCard() {
  const { user } = useAuth();

  const hour = new Date().getHours();

  let greeting = "Good Evening";

  if (hour < 12) greeting = "Good Morning";
  else if (hour < 17) greeting = "Good Afternoon";

  return (
    <section className="welcome-card">
      <div>
        <h2>
          {greeting}, {user?.name} 👋
        </h2>

        <p>
          {user?.department?.name}
        </p>

        <span>
          {user?.hostel} Hostel • Room {user?.room_no}
        </span>
      </div>
    </section>
  );
}

export default WelcomeCard;