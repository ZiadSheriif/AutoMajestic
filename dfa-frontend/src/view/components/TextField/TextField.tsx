import { Container, MyLabel } from "./TextField.styled";

interface TextFieldProps {
  login?: boolean;
  label: string;
  placeHolder: string;
  value: string | undefined;
  setValue: (value: string) => void;
  isSplitted?: boolean;
  right?: boolean;
  number?: boolean;
  disabled?: boolean;
  color?: string;
  resetBorder?: boolean;
  error?: string;
}

const TextField: React.FC<TextFieldProps> = ({
  login,
  label,
  placeHolder,
  value,
  setValue,
  isSplitted,
  number,
  color = "black",
  resetBorder = false,
  disabled = false,
  error,
}) => {
  const handleValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = event.target.value;
    if (number && /^\d*$/.test(newValue)) {
      if (newValue === "" && !login) {
        setValue("");
      } else {
        setValue(newValue);
      }
    } else {
      if (newValue === "" && !login) {
        setValue("");
      } else {
        setValue(newValue);
      }
    }
  };

  return (
    <Container login={login} isSplitted={isSplitted} resetBorder={resetBorder}>
      <MyLabel color={color}>{label}</MyLabel>
      <input
        type={"text"}
        min={number ? "0" : ""}
        placeholder={placeHolder}
        value={value ?? ""}
        onChange={handleValueChange}
        disabled={disabled}
        style={{
          cursor: disabled ? "not-allowed" : "auto",
          backgroundColor: disabled ? "#eee" : "white",
        }}
      />
      {error && (
        <MyLabel color={"red"} sx={{ fontSize: "0.8rem", paddingLeft: "1px" }}>
          {error}
        </MyLabel>
      )}
    </Container>
  );
};

export default TextField;
