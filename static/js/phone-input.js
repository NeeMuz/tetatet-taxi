const PHONE_RULES = [
    { code: '380', groups: [2, 3, 2, 2] },
    { code: '375', groups: [2, 3, 2, 2] },
    { code: '370', groups: [3, 2, 3] },
    { code: '371', groups: [2, 3, 3] },
    { code: '372', groups: [3, 4] },
    { code: '373', groups: [2, 3, 3] },
    { code: '374', groups: [2, 3, 3] },
    { code: '48', groups: [3, 3, 3] },
    { code: '49', groups: [3, 3, 4] },
    { code: '44', groups: [4, 6] },
    { code: '33', groups: [1, 2, 2, 2, 2] },
    { code: '39', groups: [3, 3, 4] },
    { code: '34', groups: [3, 3, 3] },
    { code: '90', groups: [3, 3, 4] },
    { code: '7', groups: [3, 3, 2, 2] },
    { code: '1', groups: [3, 3, 4] },
];

const E164_MAX_DIGITS = 15;

function getPhoneRule(digits) {
    const sorted = [...PHONE_RULES].sort((a, b) => b.code.length - a.code.length);
    return sorted.find((item) => digits.startsWith(item.code)) || null;
}

function maxDigitsForRule(rule) {
    return rule.code.length + rule.groups.reduce((sum, n) => sum + n, 0);
}

function formatInternationalPhone(value) {
    let digits = value.replace(/\D/g, '');
    if (!digits) return '';

    const rule = getPhoneRule(digits);
    const limit = rule ? maxDigitsForRule(rule) : E164_MAX_DIGITS;
    digits = digits.slice(0, limit);

    if (!rule) {
        if (digits.length <= 4) return '+' + digits;
        return '+' + digits.replace(/(\d{3})(?=\d)/g, '$1 ').trim();
    }

    let rest = digits.slice(rule.code.length);
    let out = '+' + rule.code;
    for (const size of rule.groups) {
        if (!rest.length) break;
        out += ' ' + rest.slice(0, size);
        rest = rest.slice(size);
    }
    return out.trim();
}

function initPhoneInput(input) {
    const format = () => {
        input.value = formatInternationalPhone(input.value);
    };

    input.addEventListener('input', format);
    input.addEventListener('focus', () => {
        if (!input.value.trim()) input.value = '+';
    });
    if (input.value.trim()) format();
}

function initPhoneInputs() {
    document.querySelectorAll('.field-input--phone').forEach(initPhoneInput);
}

document.addEventListener('DOMContentLoaded', initPhoneInputs);
