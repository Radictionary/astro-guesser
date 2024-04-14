
// change these constants
const X_MAX = 500;
const Y_MAX = 500;

const DISTANCE_MAX = 4_000_000_000;
const DISTANCE_MIN = 1_000;

// log base 10 of 40
const COEFF = X_MAX / Math.log10(DISTANCE_MAX);

// converts scale of 1000 -> DISTANCE_MAX (4 billion)
// to scale of 0 - X_MAX (500)
function logDistanceToStandard(distance) {
    return Math.log10(distance) * COEFF;
}

function logPolarToStandard(distance, ra) {
    // RA should be in degrees now
    // 4 billion -> 500
    // 1000 -> 1

    const y = distance * Math.sin(ra);
    const x = distance * Math.cos(ra);

    return { x, y };
}

function calculateClickDistance(
    origin_x, origin_y,
    click_x, click_y,
    correct_ra, correct_distance
) {
    const realX = click_x - origin_x;
    const realY = click_y - origin_y;

    const point = { x: realX, y: realY };
    const realPoint = logPolarToStandard(correct_distance, correct_ra);

    const distance = Math.sqrt((point.x - realPoint.x) ** 2 + (point.y - realPoint.y) ** 2);

    return distance;
}

function calculateScore(distance) {
    // 500 -> 0
    // 0 -> 1
    const normalizedDistance = distance / X_MAX;
    const score = 1 - normalizedDistance;
    return Math.max(score, 0);
}

function clickScore(
    origin_x, origin_y,
    click_x, click_y,
    correct_ra, correct_distance
) {
    const distance = calculateClickDistance(
        origin_x, origin_y,
        click_x, click_y,
        correct_ra, correct_distance
    );

    return calculateScore(distance);
}