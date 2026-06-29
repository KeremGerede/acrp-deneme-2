export function formatUserName(user) {
    if (!user || !user.firstName || !user.lastName) {
        return "Unknown User";
    }

    return `${user.firstName} ${user.lastName}`;
}

export function isActiveUser(user) {
    if (!user) {
        return false;
    }

    return user.status === "active";
}