import React, { useEffect, useState } from "react";
import style from "./psychologyuser.module.scss";

interface User {
  userId: string;
  email: string;
  role: string;
}

const User = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [editUserId, setEditUserId] = useState<string | null>(null); // For handling edits

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch(
          "http://localhost:5000/api/allusers/users"
        );
        const data = await response.json();
        setUsers(data);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);

  const handleDelete = async (userId: string, role: string) => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/allusers/users/${userId}`,
        {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ role }), // Send the role with delete request
        }
      );
      if (response.ok) {
        setUsers(users.filter((user) => user.userId !== userId)); // Remove user from state after deletion
      }
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  const handleEdit = async (userId: string, email: string, role: string) => {
    const newEmail = prompt("Enter new email:", email);
    if (newEmail && newEmail !== email) {
      try {
        const response = await fetch(
          `http://localhost:5000/api/allusers/users/${userId}`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: newEmail, role }),
          }
        );
        if (response.ok) {
          setUsers(
            users.map((user) =>
              user.userId === userId ? { ...user, email: newEmail } : user
            )
          );
        }
      } catch (error) {
        console.error("Error editing user:", error);
      }
    }
  };

  return (
    <div>
      <h2 className={style.userTitle}>LIST OF USERS</h2>
      <table className={style.table}>
        <thead>
          <tr>
            <th className={style.th}>User ID</th>
            <th className={style.th}>Email</th>
            <th className={style.th}>Role</th>
            <th className={style.th}>Actions</th> {/* New column for buttons */}
          </tr>
        </thead>
        <tbody>
          {users.length > 0 ? (
            users.map((user) => (
              <tr key={user.userId}>
                <td className={style.td}>{user.userId}</td>
                <td className={style.td}>{user.email}</td>
                <td className={style.td}>{user.role}</td>
                <td className={style.td}>
                  <button
                    onClick={() =>
                      handleEdit(user.userId, user.email, user.role)
                    }
                  >
                    Edit
                  </button>
                  <button onClick={() => handleDelete(user.userId, user.role)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={4} className={style.td}>
                No users found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default User;
