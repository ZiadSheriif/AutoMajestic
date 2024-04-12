import * as EmailValidator from "email-validator";

export const testEmail = (email: string) => {
  return EmailValidator.validate(email);
};
