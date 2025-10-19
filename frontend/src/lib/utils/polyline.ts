/**
 * Decode Google Maps encoded polyline
 * Based on the Encoded Polyline Algorithm Format
 * https://developers.google.com/maps/documentation/utilities/polylinealgorithm
 */
export function decodePolyline(encoded: string): [number, number][] {
	const coords: [number, number][] = [];
	let index = 0;
	let lat = 0;
	let lng = 0;

	while (index < encoded.length) {
		// Decode latitude
		let shift = 0;
		let result = 0;
		let byte: number;

		do {
			byte = encoded.charCodeAt(index++) - 63;
			result |= (byte & 0x1f) << shift;
			shift += 5;
		} while (byte >= 0x20);

		const deltaLat = result & 1 ? ~(result >> 1) : result >> 1;
		lat += deltaLat;

		// Decode longitude
		shift = 0;
		result = 0;

		do {
			byte = encoded.charCodeAt(index++) - 63;
			result |= (byte & 0x1f) << shift;
			shift += 5;
		} while (byte >= 0x20);

		const deltaLng = result & 1 ? ~(result >> 1) : result >> 1;
		lng += deltaLng;

		// Add coordinate pair (convert to degrees)
		coords.push([lat / 1e5, lng / 1e5]);
	}

	return coords;
}

/**
 * Encode coordinates to Google Maps polyline format
 * Useful for testing or sending data back to APIs
 */
export function encodePolyline(coords: [number, number][]): string {
	let encoded = '';
	let prevLat = 0;
	let prevLng = 0;

	for (const [lat, lng] of coords) {
		const encodedLat = encodeValue(Math.round(lat * 1e5) - prevLat);
		const encodedLng = encodeValue(Math.round(lng * 1e5) - prevLng);

		encoded += encodedLat + encodedLng;

		prevLat = Math.round(lat * 1e5);
		prevLng = Math.round(lng * 1e5);
	}

	return encoded;
}

function encodeValue(value: number): string {
	let encoded = '';
	let num = value < 0 ? ~(value << 1) : value << 1;

	while (num >= 0x20) {
		encoded += String.fromCharCode((0x20 | (num & 0x1f)) + 63);
		num >>= 5;
	}

	encoded += String.fromCharCode(num + 63);
	return encoded;
}
