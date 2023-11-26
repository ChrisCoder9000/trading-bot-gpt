import styled from "styled-components";

export const StyledHome = styled.main`
  padding-inline: 10%;
  box-shadow: 20px 0px 20px 6px inset rgba(0, 0, 0, 1);
  margin-bottom: 10rem;

  .hero-section {
    height: 80vh;
    display: flex;
    align-items: center;
    position: relative;

    h1 {
      font-size: 4.4rem;
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 1rem;
      width: 60%;
    }

    .world-image {
      width: 75rem;
      height: 50rem;
      position: absolute;
      right: -33rem;
      z-index: -1;
    }
  }

  .search-asset-container {
    margin-top: 10rem;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .analysis-title {
      font-size: 2.4rem;
      font-weight: 700;
      margin-bottom: 0.7rem;
    }

    .cta-section {
      .cta-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.7rem;
      }

      .cta-subtitle {
        opacity: 0.8;
        margin-top: 0;
        font-size: 0.8rem;
      }

      .input-container {
        margin-top: 0.7rem;
        display: flex;

        input {
          width: 100%;
          padding: 0.9rem 1.2rem;
          border-radius: 0.5rem;
          border: 1.5px solid #ccc;
          font-size: 1rem;
          outline: none;
          width: 15rem;
        }

        button {
          padding: 0.9rem 1.2rem;
          border-radius: 0.5rem;
          border: 1.5px solid #ccc;
          background-color: #000;
          color: #fff;
          font-size: 1rem;
          cursor: pointer;
          outline: none;
          margin-left: 1rem;
        }
      }
    }

    .search-result-table {
      width: 50%;
      padding: 3rem;
      border-radius: 1rem;
      border: 1.5px solid #ccc;

      .description {
        opacity: 0.9;
        font-size: 0.9rem;
        font-family: monospace;
      }

      .wrapper-cells {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 2rem;

        div {
          h3 {
            margin-top: 0.7rem;
          }

          p {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-top: 0.3rem;
            font-family: monospace;
            font-weight: normal;
          }
        }
      }
    }
  }
`;
