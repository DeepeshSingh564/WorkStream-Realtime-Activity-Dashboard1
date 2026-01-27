// <script>
  const tokenKey = "token";
  const tableBody = document.getElementById("activityTable");

  // ✅ Check if logged in before loading dashboard
  function getToken() {
      return localStorage.getItem(tokenKey);
  }

  const currentToken = getToken();
  if (!currentToken || currentToken === 'null') {
      alert("⚠️ Please log in first!");
      window.location.href = "/login/"; // redirect to login page
  }

  // 🔄 Load initial activities
  async function loadActivities() {
      try {
          const res = await fetch("/api/activities/", {
              headers: {
                  "Authorization": "Token " + getToken()
              }
          });

          if (res.ok) {
              const data = await res.json();
              tableBody.innerHTML = "";
              // Ensure data is an array before calling forEach
              if (Array.isArray(data)) {
                  data.forEach(log => addRow(log));
              } else {
                  console.error("API returned non-array data:", data);
              }
          } else {
              console.error("Failed to load activities:", res.status, await res.text());
          }
      } catch (error) {
          console.error("Error loading activities:", error);
      }
  }
  

  // Add row to table
  function addRow(log) {
      const row = document.createElement("tr");
      row.classList.add("activity-row");
      // Status badge - handle pending, active, and other statuses
      let statusHtml = "";
      if (log.status === "active") {
          statusHtml = `<span class="status-indicator status-active">Active</span>`;
      } else if (log.status === "pending") {
          statusHtml = `<span class="status-indicator status-pending">Pending</span>`;
      } else {
          statusHtml = `<span class="status-indicator status-inactive">Inactive</span>`;
      }
      row.innerHTML = `
          <td><span class="user-badge">${log.user}</span></td>
          <td>${log.activity_name}</td>
          <td>${log.duration} mins</td>
          <td>${new Date(log.timestamp).toLocaleString()}</td>
          <td>${statusHtml}</td>
      `;
      tableBody.prepend(row);
      updateActivityCount();
  }
  
// success feedback function
  function showSuccessFeedback() {
      const successFeedback = document.getElementById('successFeedback');
      successFeedback.classList.add('show');

      // Auto-hide after 3 seconds
      setTimeout(() => {
          successFeedback.classList.remove('show');
      }, 3000);
  }

  // ✅ WebSocket for real-time updates
  const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
  const chatSocket = new WebSocket(
      ws_scheme + '://' + window.location.host + '/ws/activities/?token=' + currentToken
  );

  chatSocket.onopen = () => {
      console.log("✅ WebSocket connected!");
  };

  chatSocket.onerror = (e) => {
      console.error("❌ WebSocket error:", e);
  };

  chatSocket.onclose = (e) => {
      console.log("🔌 WebSocket closed:", e);
  };

  chatSocket.onmessage = function(event) {
      console.log("📨 WebSocket message:", event.data);
      try {
          const msg = JSON.parse(event.data);

          if (msg.type === "activity") {
              console.log("🎯 New activity received:", msg.data);
              addRow(msg.data);
          } else if (msg.type === "connection") {
              console.log("🔗 Connection status:", msg.message, "Authenticated:", msg.authenticated);
          }
      } catch (e) {
          console.error("❌ Error parsing WebSocket message:", e);
      }
  };

  // ✅ Handle activity form submit
  document.getElementById("activityForm").addEventListener("submit", async function(e) {
      e.preventDefault();

      const name = document.getElementById("activityName").value;
      const duration = document.getElementById("duration").value;

      const response = await fetch("/api/activities/", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "Authorization": "Token " + getToken()
          },
          body: JSON.stringify({ activity_name: name, duration: duration })
      });

      if (response.ok) {
          document.getElementById("activityName").value = "";
          document.getElementById("duration").value = "";
          console.log("✅ Activity logged!");
          showSuccessFeedback();
      } else {
          console.error("❌ Failed to log activity", await response.text());
      }
  });
  // Logout button handler
  document.getElementById('logoutBtn').addEventListener('click', function() {
      if (confirm('Are you sure you want to logout?')) {
         // Handle logout logic here
          localStorage.removeItem(tokenKey);
         window.location.href = '/login/'; // redirect to login page
     }
  });

  // 🔄 Initial load
  loadActivities();
  updateActivityCount();


  function updateActivityCount() {
  const rows = document.querySelectorAll(".activity-row");
  const countEl = document.getElementById("activity-count");

  if (!countEl) return;

  const count = rows.length;
  countEl.innerText = `${count} activities`;
}
