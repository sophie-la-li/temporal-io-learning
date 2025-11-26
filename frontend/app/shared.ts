
export const testJson = (input: string) => {
    try {
        JSON.parse(input);
    } catch (e) {
        return false;
    }
    return true;
};
